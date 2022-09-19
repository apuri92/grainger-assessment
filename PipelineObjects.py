import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.utils.validation import check_is_fitted
import warnings
import logging
logging.basicConfig(format='%(asctime)s  %(name)s  %(levelname)s: %(message)s')

def set_log_level(level):
  logging.getLogger('PipelineLogger').setLevel(level)

def log_in_out(func):
  def decorated_func(*args, **kwargs):
    logger = logging.getLogger('PipelineLogger')
    logger.info(f'Entering {func.__qualname__}')
    result = func(*args, **kwargs)
    logger.info(f'Leaving {func.__qualname__}')      
    return result
  return decorated_func


# Custom transformer to select the input features. Any potentially useful features and their expected data types are set here
class FeatureSelector(BaseEstimator, TransformerMixin):
  def __init__(self, features):
    self.features = features
    self.feature_types = {
      'IssueDate': 'datetime64[ns]',
      'IssueTime': 'float',
      'MarkedTime': 'float',
      'PlateExpiration': 'float',
      'Agency': 'float',
      'Fine': 'float',
      'Latitude': 'float',
      'Longitude': 'float',
      'StatePlate': 'category',
      'BodyStyle': 'category',
      'Color': 'category',
      'ViolationDesc': 'category',
      'ViolationCode': 'category',
      'Route': 'category'
    }

    # Check if types are available. A warning is issued if a feature is used that does not have its type explicitly set
    for _ in self.features:
      if _ not in self.feature_types:
        warnings.warn(f'Feature: "{_}" not in feature_types dict', RuntimeWarning, stacklevel=2)
    return
  
  @log_in_out
  def fit(self, X, y=None):
    self.feature_names_in_ = self.features
    return self
  
  @log_in_out
  def transform(self, X, y=None, drop_cols=True):
    X_ = X[self.features].copy()
    X_ = self.set_dtypes(X_)
    return X_
  
  def set_dtypes(self, X):
    X_ = X.copy()
    for _ in self.features:
      # if feature type is not set explicitly set to object
      X_[_] = X[_].astype(self.feature_types.get(_, 'object'))
    return X_


# For categories that are fragmented, this transformer aggregates them as 'Other'. It can also change a categorical variable to a numerical one by using its frequency.
class CategoryAggregator(BaseEstimator, TransformerMixin):
  def __init__(self, cols, threshold=0.95, convert_num=False):
    self.cols = cols
    self.threshold = threshold
    self.convert_num = convert_num
    return
  
  @log_in_out
  # Build replacement dict here
  def fit(self, X, y=None):
    # self.agg_dict_ = {}
    # self.num_agg_dict_ = {}

    # for col_name in self.cols:
    #   self.agg_dict_[col_name] = self.create_col_dict(X[col_name], self.threshold)

    # # once the replacement happens, then get the counts for how many time each value occurs
    # X_ = X.replace(self.agg_dict_).copy()
    # for col_name in self.cols:
    #   self.num_agg_dict_[col_name] = self.create_num_dict(X_[col_name])

    self.agg_dict_ = self.create_agg_dict(X[self.cols], self.threshold)
    self.agg_num_dict_ = self.create_agg_num_dict(X[self.cols])

    return self

  @log_in_out
  # Apply replacement dict here
  def transform(self, X, y=None, drop_cols=True):
    # Exit if the agg dictionaries have not been created
    check_is_fitted(self)
    
    # Create a copy on which the transformations will be done
    X_ = X.copy()
    
    # if a new value is seen, that will be treated as an 'Other' category.
    for col_name in self.cols:
      for val in X[col_name].unique():
        if val not in self.agg_dict_[col_name]:
          self.agg_dict_[col_name][val] = 'Other'

    # Set all values above threshold as 'Other' and set type to 'category'
    X_.replace(self.agg_dict_, inplace=True)
    X_ = X_.astype({_: 'category' for _ in self.cols})
    
    # If convert_num is True, replace the categories with their respective frequenceis and set type to 'float'
    if self.convert_num:
      X_.replace(self.num_agg_dict_, inplace=True)
      X_ = X_.astype({col_name: 'float' for col_name in self.cols})

    return X_
  
  def create_agg_num_dict(self, X):
    # This will only work if agg_dict_ is available so we have to ensure the transformer is fit
    check_is_fitted(self)
    
    X_ = X.replace(self.agg_dict_).copy()
    agg_dict = {}
    for col in X_.columns:
      agg_dict[col] = X_[col].value_counts(dropna=False).to_dict()
    return agg_dict


  def create_agg_dict(self, X, threshold):
    agg_dict = {}
    
    # For each column, get the counts above which categories will be converted to 'Other
    for col in X.columns:
      col_vals = X[col]
      col_dict = {}
      s=0
      
      threshold_value=int(threshold*len(col_vals))
      counts=col_vals.value_counts(dropna=False, ascending=False)
      
      # If the max frequency in this column is greater than the threshold, then everything will be set to 'Other', issue a warning in such a case
      if counts[0] > threshold_value:
        warnings.warn(f'Max frequency in {col_vals.name} ( {counts.index[0]}: {counts[0]} ) is greater than threshold ({threshold_value}) . All values will be set to 0.', RuntimeWarning, stacklevel=2)
      
      # Start adding up the frequencies and build a replacement dictionary. Once the global sum has reached the threshold value, all the remaining values will be grouped as Other. 
      for i,val in counts.iteritems():
        s+=val
        if s <= threshold_value:
          col_dict[i] = i
        else:
          col_dict[i] = 'Other'

      # add the current col replacement dict to the global one
      agg_dict[col] = col_dict
    
    return agg_dict


  # # Create a dict for 
  # def create_num_dict2(self, col_vals):
  #   return col_vals.value_counts(dropna=False).to_dict()


  # def create_col_dict2(self, col_vals, threshold):
  #   col_dict = {}
  #   threshold_value=int(threshold*len(col_vals))
  #   counts=col_vals.value_counts(dropna=False, ascending=False)
  #   s=0
  #   #Check if the global sum has reached the threshold value, if so all the remaining values will be grouped as Other    

  #   if counts[0] > threshold_value:
  #     warnings.warn(f'Max frequency in {col_vals.name} ( {counts.index[0]}: {counts[0]} ) is greater than threshold ({threshold_value}) . All values will be set to 0.', RuntimeWarning, stacklevel=2)
  #   for i,val in counts.iteritems():
  #     s+=val
  #     if s <= threshold_value:
  #       col_dict[i] = i
  #     elif s > threshold_value:
  #       col_dict[i] = 'Other'
  #   return col_dict
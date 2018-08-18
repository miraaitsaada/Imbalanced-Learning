#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from random import randint, shuffle

class imbalance :
    """
        For binary data
        Coming improvements : exceptions, 
    """
    
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels
        
        self.labels_size = self.labels.shape[0]
        unique, counts = np.unique(self.labels, return_counts=True)
        self.count = dict(zip(unique, counts))
        
        value_1 = list(self.count.keys())[0]
        value_2 = list(self.count.keys())[1]
            
        if self.count[value_1] >= self.count[value_2]:
            self.prevalent = value_1
            self.non_prevalent = value_2
            self.prevalence_ratio = self.count[value_1] / self.labels_size
        else:
            self.prevalent = value_2
            self.non_prevalent = value_1
            self.prevalence_ratio = self.count[value_2] / self.labels_size
            
    def get_prevalent_value(self):
        return self.prevalent
        
    def get_prevalence_ratio(self):
        return self.prevalence_ratio
    
    def is_imbalanced(self, prevalence_ratio):
        if prevalence_ratio < 0.5 :
            prevalence_ratio = 1 - prevalence_ratio
            
        if self.prevalence_ratio >= prevalence_ratio:
            return True
        return False
    
    def random_unique_list(self, low, high, size):
        """
            if the size is bigger than the number of possible values, then return shuffled integers between lower and upper bound.
        """
        if size > (high-low) :
            print("Too large size !")
            l = list(range(low, high))
            shuffle(l)
            return l
        
        if size == (high-low) :
            l = list(range(low, high))
            shuffle(l)
            return l
        
        elements = set()
        while len(elements) < size :
            elements.add(randint(low, high-1))
            
        l = list(elements)
        shuffle(l)
            
        return l
    
    def random_unique_samples(self, data, size):
        saved_indices = self.random_unique_list(0, len(data), size)
        
        return data[saved_indices]
        
    
    def random_under_sampling(self, prevalence_ratio = 0.5):
        """
            Param : data features
                    binary assumed labels
            Return : random under-sampled data and labels w.r.t. desired ratio
        """
        
        if self.prevalence_ratio <= prevalence_ratio:
            print("No need of under-sampling")
            return (self.data, self.labels)
        
        num_non_prevalent = (1 - self.prevalence_ratio) * self.labels_size
        num_saved_samples = (num_non_prevalent * prevalence_ratio) / (1 - prevalence_ratio)
        
        print("non-prel" , num_non_prevalent)
        print("prel" , num_saved_samples)
        
        prevalent_labels_indices = np.where([self.labels == self.prevalent])[1]
        other_labels_indices = np.where([self.labels == self.non_prevalent])[1]
        
        saved_indices = self.random_unique_samples(prevalent_labels_indices, size = num_saved_samples)
        
        saved_labels = self.labels.loc[saved_indices]
        saved_data = self.data.loc[saved_indices]
        
        under_sampled_labels = pd.concat([saved_labels, self.labels.loc[other_labels_indices]])
        under_sampled_data = pd.concat([saved_data, self.data.loc[other_labels_indices]])
        
        return (under_sampled_data, under_sampled_labels)
    
    
if __name__ == "__main__":
    
    data_size = 1000
    id = np.array(range(0, data_size))
    feature1 = np.random.randint(1, 20, data_size)
    feature2 = np.random.randint(5, 10, data_size)
    labels = np.random.randint(0, 2, data_size)
    
    arr = np.vstack((id, feature1, feature2, labels)).T
    
    dataset = pd.DataFrame(arr, columns = ["id", "feature1", "feature2", "labels"])
    
    print(dataset)
    
    labels = dataset["labels"]
    del dataset["labels"]
    
    imb = imbalance(dataset, labels)
    
    imb.is_imbalanced(0.15) #works
    imb.get_prevalence_ratio() #works
    imb.get_prevalent_value() #works
    
    d, l = imb.random_under_sampling(prevalence_ratio = 0.5)
    
    unique, counts = np.unique(labels, return_counts=True)
    count = dict(zip(unique, counts))
    print("labels :"  , count)
        
    unique, counts = np.unique(l, return_counts=True)
    count = dict(zip(unique, counts))
    print("l : ", count)
    
    x = pd.concat([d, l], axis=1)
    
    
    
    
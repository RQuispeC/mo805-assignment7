import numpy as np
import os.path  as osp
import matplotlib.pyplot as plt

def read_file(file_path):
  f = open(file_path, "r")
  data = []
  for line in f:
    data.append(line)
  return np.array(data)

def load_data(names_file, features_dir):
  ms_features = []
  ss_features = []
  ids = []
  names = read_file(names_file)
  names.sort()
  last_class = ""
  class_id = 0
  for name in names:
    name = name[:-1] #remove new line end
    ms_file_path = osp.join(features_dir, name + "_MS.txt")
    ss_file_path = osp.join(features_dir, name + "_SS.txt")
    ms_data = read_file(ms_file_path)
    ss_data = read_file(ss_file_path)
    ms_data = ms_data.astype(np.float)
    ss_data = ss_data.astype(np.float)
    ms_features.append(ms_data)
    ss_features.append(ss_data)
    data_class = name.split("-")[0]
    if data_class != last_class:
      last_class = data_class
      class_id += 1
    ids.append(class_id)

  ids = np.array(ids)
  names = np.array(names)
  ms_features = np.array(ms_features)
  ss_features = np.array(ss_features)
  return ids, names, ms_features, ss_features

def dist(query_features, gallery_features):
  matrix = np.zeros((len(query_features), len(gallery_features)))
  q_pow = np.sum(query_features * query_features, axis = 1)
  g_pow = np.sum(gallery_features * gallery_features, axis = 1)
  prod = 2 * np.dot(query_features, np.transpose(gallery_features))
  matrix += np.transpose(np.tile(q_pow, (len(g_pow), 1)))
  matrix += np.tile(g_pow, (len(q_pow), 1))
  matrix -= prod
  return matrix

def precision_recall(distmat, q_ids, g_ids, max_rank = 20, gt_samples = 20):
  indices = np.argsort(distmat, axis=1)
  matches = (g_ids[indices] == q_ids[:, np.newaxis]).astype(np.int32)
  cnt = matches.cumsum(axis = 1)[:, :max_rank]

  den_precision = np.tile(np.arange(1, max_rank + 1), (len(q_ids), 1))
  den_recall = np.full((len(q_ids), max_rank), gt_samples)
  precision = cnt / den_precision
  recall = cnt / den_recall

  precision = np.average(precision, axis = 0)
  recall = np.average(recall, axis = 0)
  return precision, recall

if __name__ == '__main__':
  ids, names, ms_features, ss_features = load_data("MO445-descriptors/examples/names.txt", "MO445-descriptors/examples/mpeg7_features/")

  max_rank = 1400
  dismat_MS = dist(ms_features, ms_features)
  pms, rms = precision_recall(dismat_MS, ids, ids, max_rank=max_rank)

  dismat_SS = dist(ss_features, ss_features)
  pss, rss = precision_recall(dismat_SS, ids, ids, max_rank=max_rank)

  print("Generating Precision x Recall curve")
  plt.title('Methods comparison - MO805 - Assignment 7')
  plt.plot(rms, pms, label = 'Multiscale fractal dimension')
  plt.plot(rss, pss, label = 'Segment saliences')
  plt.legend(loc = 'upper right')
  plt.xlim([0, 1])
  plt.ylim([0, 1])
  plt.ylabel('precision')
  plt.xlabel('recall')
  plt.savefig("precision_recall.png")
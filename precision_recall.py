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
  #ids, names, ms_features, ss_features = load_data("MO445-descriptors/examples/names.txt", "MO445-descriptors/examples/mpeg7_features/")
  ids = np.array([0, 0, 0 , 0, 0, 1, 1, 1, 1, 1])
  features_1 = np.array([[1.5, 2.5],
                      [1.5, 2.0],
                      [2.0, 2.0],
                      [1.0, 2.0],
                      [1.5, 1.5],
                      [1.0, 1.0],
                      [1.0, 2.0],
                      [1.0, 3.0],
                      [1.0, 4.0],
                      [1.0, 5.0]])

  features_2 = np.array([[2, 1],
                      [2.0, 2.0],
                      [2.0, 3.0],
                      [2.0, 4.0],
                      [2.0, 5.0],
                      [1.4, 1.4],
                      [1.6, 1.4],
                      [1.6, 1.2],
                      [1.4, 1.2],
                      [1.5, 1.3]])

  features_3 = np.array([[1.5, 2.5],
                      [1.5, 2.0],
                      [1.75, 2.25],
                      [1.25, 2.0],
                      [1.5, 1.5],
                      [1.5, 5.5],
                      [1.25, 5.0],
                      [1.5, 5.0],
                      [1.15, 5.0],
                      [1.5, 4.5]])

  max_rank = 10
  dismat_1 = dist(features_1, features_1)
  dismat_2 = dist(features_2, features_2)
  dismat_3 = dist(features_3, features_3)
  p_1, r_1 = precision_recall(dismat_1, ids, ids, max_rank=max_rank, gt_samples=5)
  p_2, r_2 = precision_recall(dismat_2, ids, ids, max_rank=max_rank, gt_samples=5)
  p_3, r_3 = precision_recall(dismat_3, ids, ids, max_rank=max_rank, gt_samples=5)

  print("Generating Precision x Recall curve")
  plt.title('MO805 - Test 1 - question 4')
  plt.plot(r_1, p_1, label = 'Descriptor 1',  linestyle="-")
  plt.plot(r_2, p_2, label = 'Descriptor 2',  linestyle="--")
  plt.plot(r_3, p_3, label = 'Descriptor 3',  linestyle="-.")
  plt.legend(loc = 'lower left')
  plt.xlim([0, 1.01])
  plt.ylim([0, 1.01])
  plt.ylabel('precision')
  plt.xlabel('recall')
  plt.savefig("precision_recall.png")
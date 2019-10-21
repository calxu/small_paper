#!/bin/bash

echo """
Task: Output train and test data.
Author: Calvin,Xu.
"""

# Extract part US Checkin data.
python3 0_extract_US_data.py
echo "Task 0 complete."

# Get users_ID and train checkins.
python3 1_get_usersID_trainCheckins.py 10
echo "Task 1 complete."

# Get train_UsersID and test_UsersID file
python3 2_get_train_test_usersID.py 0.80      # 80% as train set, and 20% as test set
echo "Task 2 complete."

# Get positive_Examples file, and remove users_ID 
python3 3_get_positive_examples.py
echo "Task 3 complete."

# Get train_Positives and test_Positives file, and remove positive_Examples
python3 4_get_train_test_positive.py
echo "Task 4 complete."

# Get train_Negatives and test_Negatives file, and remove train_usersID and test_usersID
cat graph | python3 5_get_negative_graph.py
rm users_ID
rm train_UsersID test_UsersID
rm positive_Examples
rm global_Positive_Examples global_users_ID
echo "Task 5 complete."

# Get train_Data and test_Data file, and remove train_Positives, train_Negatives, test_Positives and test_Negatives
python3 6_shuffle.py train
python3 6_shuffle.py test
# rm train_Positives train_Negatives test_Positives test_Negatives
echo "Task 6 complete."

# cp train_* ../2_Train/ ; cp test_Data ../4_Fusion/

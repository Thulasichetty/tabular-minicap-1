import pandas as pd
import argparse
from cryptography.fernet import Fernet
from io import StringIO
from sklearn.metrics import f1_score


def main(key):
	func = Fernet(key)

	# read encrypted file
	with open("encrypted_test_actuals.csv", "rb") as enc_handler:
		encrypted_file = enc_handler.read()


	# read submission file
	submission = pd.read_csv("submission.csv")


	# decrypt the file
	decrypted_file = func.decrypt(encrypted_file)

	# convert encrypted file to pandas dataframe
	csvIO = StringIO(decrypted_file.decode())
	test_actual = pd.read_csv(csvIO)

	# some assertion checks
	if "is_promoted" not in submission.columns:
		raise ValueError("is_promoted column not present")
	if submission.shape[0] != test_actual.shape[0]:
		print(submission.shape, test_actual.shape)
		raise ValueError("Different number of rows present")
	if (len(set(submission.employee_id)-set(test_actual.employee_id)) > 0) or (len(set(test_actual.employee_id)-set(submission.employee_id))>0):
		raise ValueError("employee_id mismatch")

	submission = submission.sort_values("employee_id").reset_index(drop=True)
	test_actual = test_actual.sort_values("employee_id").reset_index(drop=True)

	# find f1 score
	result = f1_score(test_actual['is_promoted'], submission['is_promoted'])
	return result


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-k", "--key", required=True)
	args = parser.parse_args()
	result = main(args.key)
	print(result)
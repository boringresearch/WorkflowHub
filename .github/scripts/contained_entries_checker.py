import unittest
import os
import json

class TestSubentries(unittest.TestCase):
    def load_json_with_duplicate_keys_check(self, filepath):
        duplicate_keys = []

        def check_duplicate_keys(pairs):
            keys = [pair[0] for pair in pairs]
            if len(keys) != len(set(keys)):
                for key in keys:
                    if keys.count(key) > 1 and key not in duplicate_keys:
                        duplicate_keys.append(key)
            return dict(pairs)

        try:
            with open(filepath, 'r') as file:
                data = json.load(file, object_pairs_hook=check_duplicate_keys)
            return data, duplicate_keys
        except json.JSONDecodeError as e:
            assert False, f"Error: The {filepath} file is not a valid JSON file. Error details: {str(e)}"

    def test_subentries(self):
        # Load the data from the data_axs.json file in the root directory
        data_file = './data_axs.json'
        data, duplicate_keys = self.load_json_with_duplicate_keys_check(data_file)

        # If data is None, JSON was invalid
        if data is None:
            return

        # Assert no duplicate keys
        self.assertEqual(len(duplicate_keys), 0, f"Error: Duplicate keys {duplicate_keys} found in data_axs.json")

        # Get the folders in the root directory
        folder_names = [name for name in os.listdir('./') if os.path.isdir(name)]

        # Compare folder names with contained_entries
        self.assertSetEqual(set(data['contained_entries'].keys()), set(folder_names), "Error: Folders and contained_entries should match.")

if __name__ == "__main__":
    unittest.main()

import json
import unittest


def count_module_key(modules, key):
    """Helper function to count occurrences of a given key in all module dictionaries."""
    return sum(1 for module in modules if key in module and module[key])


class TestModulesJson(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the class by reading and parsing the modules.json file."""
        with open('./modules.json', 'r', encoding='utf-8') as f:
            cls.modules_content = f.read()

    def test_valid_json(self):
        """Test that modules.json contains valid JSON."""
        try:
            json.loads(self.modules_content)
        except json.JSONDecodeError:
            self.fail("modules.json is not valid JSON.")

    def test_required_keys(self):
        """Test that each module has all required keys."""
        parsed_modules = json.loads(self.modules_content)
        modules_count = len(parsed_modules)
        name_count = count_module_key(parsed_modules, 'name')
        description_count = count_module_key(parsed_modules, 'description')
        github_url_count = count_module_key(parsed_modules, 'githubUrl')

        self.assertEqual(name_count, modules_count, "Not all modules have a 'name' key.")
        self.assertEqual(description_count, modules_count, "Not all modules have a 'description' key.")
        self.assertEqual(github_url_count, modules_count, "Not all modules have a 'githubUrl' key.")

    def test_uniqueness(self):
        """Test that all module names are unique."""
        parsed_modules = json.loads(self.modules_content)
        modules_count = len(parsed_modules)

        # Create a set of unique module names
        module_names = [module['name'] for module in parsed_modules]
        unique_module_names = set(module_names)
        unique_modules_count = len(unique_module_names)

        self.assertEqual(modules_count, unique_modules_count, "Module names are not unique.")


if __name__ == '__main__':
    unittest.main()
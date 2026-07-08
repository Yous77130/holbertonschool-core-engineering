from tools.file_writer import save_study_guide

if __name__ == "__main__":
    test_content = "# Test\nCeci est un test d'écriture déterministe."
    result = save_study_guide(test_content)
    print(result)
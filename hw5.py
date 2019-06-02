import numpy as np
import pandas as pd
import pathlib
from matplotlib import pyplot as plt
from typing import Union
from typing import Tuple
from validate_email import validate_email

class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """
    def __init__(self, data_fname: Union[pathlib.Path, str]): #type hinting (doesn't make it str), union: can be both str or path, -> hinting for functions
        data_fname = pathlib.Path(data_fname)
        #validate that the file exits
        assert data_fname.exists()
        # Checking that the file name is str or Path
        if not isinstance(data_fname, (str, pathlib.Path)):
            raise TypeError("The file name must be str or pathlib.Path")
        self.data_fname = data_fname
        
          
    def read_data(self):
        """
        Reads the json data located in self.data_fname into memory, to
        the attribute self.data.
        """
        self.data = pd.read_json(self.data_fname)
        print(self.data)

    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculates and plots the age distribution of the participants.
        Returns a tuple containing two numpy arrays:
        The first item being the number of people in a given bin.
        The second item being the bin edges.
        """
        age_array = self.data['age']
        self.dist = plt.hist(age_array[~np.isnan(age_array)], bins=[0,10,20,30,40,50,60,70,80,90,99]) 
        plt.show(block=False)
        return (self.dist[0],self.dist[1])

    def remove_rows_without_mail(self) -> pd.DataFrame:
        """
        Checks self.data for rows with invalid emails, and removes them.
        Returns the corrected DataFrame, i.e. the same table but with
        the erroneous rows removed and the (ordinal) index after a reset.
        """
        # Remove empty rows
        self.data = self.data.dropna(axis=0, subset=['email'])
        # Remove rows with invalid email addresses
        self.data['is_valid_email'] = self.data['email'].apply(lambda x:validate_email(x))
        return self.data[self.data.is_valid_email == False]

    def fill_na_with_mean(self) -> Union[pd.DataFrame, np.ndarray]:
        """
        Finds, in the original DataFrame, the subjects that didn't answer
        all questions, and replaces that missing value with the mean of the
        other grades for that student. Returns the corrected DataFrame,
        as well as the row indices of the students that their new grades
        were generated.
        """
        mask = self.data.loc[:,['q1','q2','q3','q4','q5']].isnull().any(axis='columns')
        row_nums = np.where(mask==True)
        return self.data.fillna(self.data.mean()), row_nums
        


#df = QuestionnaireAnalysis('data.json')
#fn = pathlib.Path('C:/Users/Liz/Dropbox/LabDropbox/Liz/studies/PythonCourse/hw5_2019/data.json')
F = QuestionnaireAnalysis('C:/Users/Liz/Dropbox/LabDropbox/Liz/studies/PythonCourse/hw5_2019/data.json')
F.read_data()
F.show_age_distrib()
F.remove_rows_without_mail()
F.fill_na_with_mean()



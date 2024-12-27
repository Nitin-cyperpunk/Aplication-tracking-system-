# Resume-buddy
# Overview
The Resume Buddy application is a Streamlit-based tool designed to assist users in evaluating resumes against job descriptions using AI. It leverages Google's Generative AI to analyze resumes, provide feedback, and generate offer letters for top candidates.
## Features
- Resume Evaluation: Analyzes resumes based on job descriptions and provides a match percentage.
- Keyword Suggestions: Identifies missing keywords from resumes that could enhance job matching.
- Offer Letter Generation: Automatically creates PDF offer letters for selected candidates.
- User-Friendly Interface: Built with Streamlit for easy interaction.

## How to Clone the Repository
To clone this repository, use the following command in your terminal:
bash
git clone https://github.com/USERNAME/REPOSITORY_NAME.git
Replace `USERNAME` with your GitHub username and `REPOSITORY_NAME` with the name of the repository.

## How to Run the Application
1. **Install Dependencies**: Ensure you have Python installed, then navigate to the project directory and install the required packages:

pip install -r requirements.txt
2. **Set Up Environment Variables**: Create a `.env` file in the root directory of your project and add your Google API key:

GOOGLE_API_KEY=your_api_key_here
3. **Run the Application**: Start the Streamlit server by running:

streamlit run app.py
4. **Access the Application**: Open your web browser and go to `http://localhost:8501` to access the application interface.

## Usage Instructions
1. Paste the job description into the designated text area.
2. Upload resumes in PDF format using the file uploader.
3. Click on the "Submit" button to evaluate the resumes.
4. Review the output for match percentages, missing keywords, and generated offer letters.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

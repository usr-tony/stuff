
user = 'tony'
profile_path = f'../profiles/{user}/'
pdf_resume_path = profile_path + 'resume.pdf'
resume_path = profile_path + 'resume.txt'
user_info_path = profile_path + 'info.json'
applications_path = './data/applications.db'
geckodriver_path = '../geckodriver'
# undesirable companies to be excluded, usually are recruitment firms
recruiters = [
    'keegan adams',
    'hays',
    'randstad',
    'robert half',
    'michael page',
    'DFP recruitment',
    'chandler macleod',
    'bluefin resources',
    'drake international',
    'robert walters',
    'scout talent',
    'gough recruitment',
    'bolton clarke',
    'profusion pac',
    'advance human solutions',
    'mars recruitment',
    'recruitment',
]
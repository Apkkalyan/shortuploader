# shortuploader
This app can help you to upload shorts online , and saving you plenty of time on scheduling once setup properly.

TO TRY THIS CODE WORKING IN YOUR DEVICE !
1. Clone repo or import the upload_short.py file's code to your vs code.
2. if the python and pip installed in your system , it will be easy coz , the code is in python rn.
3. now , you have set up few things.
   1. First go to google cloud console.
   2. Make a account if you don't have one , its easy to navigate.
   3. Make or rename existing project with the details they placeholders asking.
        - Go to / Search for "API & Services" then select "youTube Data API V3" and enable this for you project
        - Go to /Search for "Credentials" and set up things placeholder is asking
        - They might ask you to connect a billing account or prepayment , you can do it , you can cancel payment any time from you UPI account options , and no money will be deducted , cause their are some free tier
        - After , filling the creditials details , come to "OAuth Cosent screen" > go to "Audience" > "Test user" and add some email you can use for try out the project , in my case i use my old email , from i tried to upload the shorts.
        - now , go to "Data Access" of same screen options > "add or Remove Scopes"  and choose ["https://www.googleapis.com/auth/youtube.upload"] find or add this manualy , this will help you to upload the video.
        -  This all basic stuff nessaccery to going on to start the project from google cloud console.
     
  4. Now for the files and code in you PC:
    1. First Create a File that where you will be sequencing all the video or import the videos , make sure this has the reel demension and size of file .
     2. then , copy the path , and replace with the current string in the project to the appropiate location follow comments
     3. then , copy the downloaded location path of "creaditials.json "  that you get from google cloud plateform and put in the code as step 2.
5. now , install the pakages using appropiate pip command .
6. you are well to go..

# 7. Important
 run the code using terminal ovious , cmd - open the terminal form the same folder where code exixts , and run command python shots_uploader.py ot TAB to auto enter the file name .

- loging with the same email , that you have entered in testing email and step 3.3.inner_steps.

- and the thing start doing its stuff.

- wallahhh... , go and check your youtube studio ;) !!
  
            

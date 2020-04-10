# Amazon LEX
Amazon Lex is a service for building conversational interfaces into any application using voice and text. Amazon Lex provides the advanced deep learning functionalities of automatic speech recognition (ASR) for converting speech to text, and natural language understanding (NLU) to recognize the intent of the text, to enable you to build applications with highly engaging user experiences and lifelike conversational interactions. With Amazon Lex, the same deep learning technologies that power Amazon Alexa are now available to any developer, enabling you to quickly and easily build sophisticated, natural language, conversational bots (“chatbots”).

# Real world Amazon LEX Implementation Demo
These are step by step instructions to build a chatbot using AWS LEX. We will cover some basics and implement a real-world scenario by using AWS Lambda to search through csv file hosted on AWS S3:
1.	Welcome greeting message with prompt to add name.
2.	Fulfil AWS LEX response using AWS Lambda to search through file and return output.

## Setup:
To get started, login to your AWS account. If you don’t have AWS account, you can create a free account on AWS website.

## Concepts and terminology:
Before proceeding further, lets quickly understand Amazon Lex core concepts and terminology (from AWS Documentation).
### Bot:
A bot performs automated tasks such as ordering a pizza, booking a hotel, ordering flowers, and so on. An Amazon Lex bot is powered by Automatic Speech Recognition (ASR) and Natural Language Understanding (NLU) capabilities, the same technology that powers Amazon Alexa. Amazon Lex bots can understand user input provided with text or speech and converse in natural language. You can create Lambda functions and add them as code hooks in your intent configuration to perform user data validation and fulfillment tasks.
### Intent:
An intent represents an action that the user wants to perform. You create a bot to support one or more related intents. For example, you might create a bot that orders pizza and drinks. For each intent, you provide the following required information:
+ 	Intent name– A descriptive name for the intent. For example, OrderPizza.
+ 	Sample utterances – How a user might convey the intent. For example, a user might say "Can I order a pizza please" or "I want to order a pizza".
+ 	How to fulfill the intent – How you want to fulfill the intent after the user provides the necessary information (for example, place order with a local pizza shop). We recommend that you create a Lambda function to fulfill the intent.

## Bot Build:
1.	Login to your account and on the AWS management console, search and click Amazon LEX under Find services 
![image](https://user-images.githubusercontent.com/29644699/78953419-c070d000-7aa6-11ea-8c62-f15b9cba4199.png)
2.	If you are navigating Lex for the first time, click Get started. On the next screen
+   Choose Custom bot
+ 	Enter Bot name
+ 	Select Output voice
+ 	Enter Session timeout. For this demo I am choosing 2 minutes.
+ 	Select No for COPPA from this demo prospective.
+ 	Click Create
![image](https://user-images.githubusercontent.com/29644699/78953692-bf8c6e00-7aa7-11ea-948c-ca24be7a3b38.png)
3.	On next Page 
+ 	click create intent and click Add
![image](https://user-images.githubusercontent.com/29644699/78953907-58bb8480-7aa8-11ea-9086-cef6eeca58f9.png)
+   Utterances are the spoken or typed phrase that can invoke your intent. This is the way bot invoke intent and start conversation or actions. We will start with basic greeting like Hi, Hello or Hey. Lex is powered by Natural Language Understanding (NLU) capability which means it is smart enough to recognize closely matching phrases and make sense out of it.
![image](https://user-images.githubusercontent.com/29644699/78953941-7983da00-7aa8-11ea-918e-b318180193d3.png)
+   Once Utterances are added, we will add response to our Greetings Intent. Response is the message returned by Lex Bot in return of utterances. There are some other better ways to respond using AWS Lambda, but for now we will use Response. Click Add message and enter message. Add multiple messages and Lex bot use these messages randomly to give more human touch.   
![image](https://user-images.githubusercontent.com/29644699/78953961-97513f00-7aa8-11ea-82a4-e328a8dc20c6.png)
+   Once done click on Save intent on bottom of page. With this we are ready to Build our Chatbot by clicking Build button on top right corner. It may take a minute or 2.
+   On right side of page click on Test bot and you are ready to interact with bot.
![image](https://user-images.githubusercontent.com/29644699/78953996-b8199480-7aa8-11ea-8fc0-714b9e2f2c42.png)
4.	In this section, we will make bot more interactive to accept user input using slots. Slots are used to store user input value. We will create a slot to store Username and add it as part of Bot response.
+   Under slots, create slot name as Username
+   Amazon has many built-in slots type, choose AMAZON.US_FIRST_NAME
+   Enter message in Prompt. Prompt message is the exact phrase bot will ask user.
+   Click on + sign to add slot
![image](https://user-images.githubusercontent.com/29644699/78954038-d7b0bd00-7aa8-11ea-8cd3-6219472d3688.png)
+   Now we can add slot in response to make it more personalized. To use slot use syntax {slotname}
![image](https://user-images.githubusercontent.com/29644699/78954059-e8613300-7aa8-11ea-901f-997bddc1ccb5.png)
+   Save Intent by build Bot again. Let’s test bot.
![image](https://user-images.githubusercontent.com/29644699/78954095-04fd6b00-7aa9-11ea-8317-9d6005a91d18.png)
5.	This section, we will use AWS Lambda to return the response. For this blog we will query csv file placed in AWS S3 using Bot interface. To keep this demo short, we will not be covering AWS Lambda and AWS S3 service.
+   Create bucket in S3 and upload csv file containing Employee and associated department information. Use attached fle employeeDetails.csv (Do not change name of file). 
![image](https://user-images.githubusercontent.com/29644699/78954170-3ece7180-7aa9-11ea-8a19-c75cf2568539.png)
+   We will create AWS Lambda function with language as Python3.8 or latest. Under permissions choose Create new role from AWS policy template and provide suitable role. We will add permissions in next step. After selecting all options Click Create function. After creation of function, change Timeout to 1 minute or suitable timeout under Basic settings.
![image](https://user-images.githubusercontent.com/29644699/78954258-848b3a00-7aa9-11ea-9128-19ca621516ee.png)
+   Next we are going to modify Role for Lambda to add S3 Read only access. Go to AWS IDM and select role we mentioned in previous step. Search AmazonS3ReadOnlyAccess policy and attach to role.
![image](https://user-images.githubusercontent.com/29644699/78954282-9c62be00-7aa9-11ea-97c9-7f3be7a9f112.png)
+   Next step, copy attached Lambda code file lambda_handler.py. Copy paste code in editor window. In the code replace bucket name “demoawslex” with bucket name you have created. Click save.
+   Click test to configure test event. Provide name for Event name and copy json event by referring Labda_event_test. Click create and then Test. If everything is set correctly, function should succeed. 
![image](https://user-images.githubusercontent.com/29644699/78954323-c9af6c00-7aa9-11ea-92a0-6f9b676679c9.png)
6.	In this section we will create new intent to ask user to provide department number and return employees belonging to that department by searching csv file uploaded in S3.
+   Create new Intent by clicking plus button next to Intents. Provide name of intent as “RetunEmployeeName”. This is important as Lambda code will recognize intent name to perform specific action.
![image](https://user-images.githubusercontent.com/29644699/78954395-11ce8e80-7aaa-11ea-9be1-cfb346536fce.png)
+   Provide sample utterance as department and department id.
![image](https://user-images.githubusercontent.com/29644699/78954431-30348a00-7aaa-11ea-8e80-ec26cd207492.png)
+   Next we are going to create slot with name as DepartmentID, slot type as AMAZON.NUMBER and prompt as What is Department ID?

![image](https://user-images.githubusercontent.com/29644699/78954461-4a6e6800-7aaa-11ea-8ed5-6d9a75683041.png)
+ Under Fulfillment click AWS Lambda function and choose Lambda function you have created from drop down. It will display message to provide permission to Lambda function. Click OK.
![image](https://user-images.githubusercontent.com/29644699/78954497-61ad5580-7aaa-11ea-974f-6fc36b097a13.png)
+   Click Save intent. Now we will modify response of Greetings Intent to append existing message and add phrase “I can search for employee names in a department. To continue type department”. Once done click Save intent followed by Build.

![image](https://user-images.githubusercontent.com/29644699/78954548-7b4e9d00-7aaa-11ea-8ac9-d746df667244.png)
+   With this Bot is ready to be tested.

![image](https://user-images.githubusercontent.com/29644699/78954588-94574e00-7aaa-11ea-99d1-efc154942d63.png)

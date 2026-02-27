---
author: osnowden
comments: true
date: 2020-06-25 16:41:36+00:00
layout: post
link: http://oliviasnowden.me/2020/06/25/cognitive-services-translating-speech/
slug: cognitive-services-translating-speech
title: COGNITIVE SERVICES-TRANSLATING SPEECH
tags: [code, AI, cloud]
---




In addition to text analysis Microsoft's cognitive services allow you to convert speech to text, text to speech, and even translate between spoken languages. This powerful AI service is surprisingly easy to use. I was able to speak into my computers microphone and receive a text translation in one language or a spoken translation in multiple languages --all with the [code ](https://docs.microsoft.com/en-us/learn/modules/translate-speech-speech-service/)provided on Microsoft Learn. You have the option to work with the speech SDK (software development kit) in C# or python, I choose python. 







Like the text analysis cognitive service, you'll need to deploy a resource (for the speech service, deploy the "speech" resource) in Azure and save its key/region to use in the scripts. Since working with translating speech requires you to use your computer's microphone, the code for this service needs to be executed locally instead of in an online environment like Visual Studio Codespaces. I already had python and Visual Studio Code installed on my laptop, so that is what I used. 







## Speech to text translation 







First, you need to create a folder to store the project in and then open that folder in your code editor. Once in the folder, create a file named translate_speech.py and copy in the code provided for this exercise on Microsoft Learn. In line 3 insert your Azure speech resource's key and region (To keep my key from being public I removed it for this photo-safety first). 







![](/cognitive-4.png)







This script is commented well, so its easy to walk through. It breaks down speech translation into three key objects: 







  1. SpeechTranslationConfig: accepts the key and region of your Azure resource, sets the source and target language, and creates a name for the speech output
  2. TranslationRecognizer: accepts the SpeechTranslationCofig object which calls the method to start the translation
  3. TranslationRecognitionResult: returns the result of the translation 






In this first half of this translate_speech_to_text function you can change the fromLanguage and toLanguage variables to translate to/from many different languages. Below is the second half of the function which consists of an if/elif statement that gives options for output. This way you'll receive output that informs you of what has happened even if the speech couldn't be translated or the translation was cancelled. 







![](/cognitive-5.png)







In the last line you can see the translate_speech_to_text() function being called, which in combination with your Azure resource translates your speech to another language when the script is run. Here you can see my script running which translated "Hello World" in english to "Hallo Welt" in dutch. 







![](/cognitive-6.png)







## Speech to speech translation-multiple languages 







The speech cognitive service also allows you to translate speech in one language to speech in multiple other languages using a similar script to the one shown above. In addition to the SpeechTranslationConfig, TranslationRecognizer, and TranslationRecognitionResult objects the script for translating to multiple languages also uses a speech synthesizer object that plays the audio output of the target languages. 







You can use the same speech Azure resource for this script, I used Visual Studio Code and python here too. First you need to create a new file titled texttomultilang.py or something similar. Then copy in the code provided on Microsoft Learn for this exercise. Like before, you also need to insert your speech resource's key and region before the script's function. 







![](/cognitive-7.png)







Here you can see this script is similar to the speech to text script. One difference is the addition of the speech_synthesizer object and multiple target languages in the SpeechTranslationConfig object's dictionary. You can add as many target languages as you would like by adding "speech_config.add_target_language('_language_')" to the dictionary. 







![](/cognitive-8.png)







![](/cognitive-9.png)







Another difference between this script and the speech to text script is a more complicated if/elif statement at the end of the function. So that pronunciation is correct, its important that the synthesized voice used to "speak" the translation is the right voice for the language. To make sure that happens an if/else statement for each language the speech is being translated into is nested under the first **if** in the main if/elif structure. This is the basic setup: 






    
    Is the speech recognized/can it be translated? 
       then print the translations:
        is the toLanguage language#1? 
          then use language#1's voice
        is the toLanguage language#2? 
          then use language#2's voice
    OR Could the speech not be translated? 
    OR Is the speech not recognized? 
    OR Was the translation cancelled? 
       print this error







If you add more toLanguages in the SpeechTranslationConfig's dictionary, make sure you add the language(s) to the nested if/else statement and name the right [voice](https://aka.ms/speech/sttt-languages). 







When the script is run your speech is printed, followed by the translations into the languages of your choice. In addition to a printed translation, you  receive a spoken translation with an appropriate accent. 







![](/cognitive-10.png)







Being able to translate between languages in near real-time could be used in meetings, conferences, or presentations that have participants from all over the world. Regardless of how its used, working with the speech cognitive service is great practice in using python ( or C#) to work with AI. 




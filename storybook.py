# Import
from openai import OpenAI
import streamlit as st


client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

def story_gen(prompt):
    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = [
            {'role' : 'system', 'content' : "You are a storyteller. Come up with a story based on the theme given by the user. The genre is thriller. Be sure to create a story with shocking plot twist. Your story must be within 100 words."},
            {'role' : 'user', 'content' : prompt}
        ],
        max_tokens = 1000
    )
    
    return response.choices[0].message.content

def cover_prompt(prompt):
  response = client.chat.completions.create(
      model = 'gpt-4o-mini',
      messages = [
          {'role' : 'system', 'content' : """
                                          You are tasked with generating a prompt for an AI image generator.
                                          A story will be given and you have to analyse and digest the content and extract the main elements or essence of the story.
                                          Output a short prompt to produce a good cover art for a storybook
                                          """},
          {'role' : 'user', 'content' : prompt}
      ]
  )
  
  return response.choices[0].message.content

def cover_art(prompt):
  response = client.images.generate(
      model = 'dall-e-3',
      prompt = prompt,
      size = '1024x1024',
      quality = 'standard',
      style = 'vivid',
      n = 1
  )

  return response.data[0].url

def storybook(prompt):
  story = story_gen(prompt)
  coverPrompt = cover_prompt(story)
  img = cover_art(coverPrompt)


  st.image(img)
  st.divider()
  st.caption(story)


prompt = st.text_input("Enter a theme for a storybook : ")
if(st.button("Generate story")):
    storybook(prompt)

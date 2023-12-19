import g4f

g4f.debug.logging = True  # Enable debug logging
g4f.debug.check_version = False  # Disable automatic version checking
print(g4f.Provider.Bing.params)  # Print supported args for Bing

# # Using automatic a provider for the given model
# ## Streamed completion
# response = g4f.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "user", "content": "Hello"}],
#     stream=True,
# )
# for message in response:
#     print(message, flush=True, end='')

# ## Normal response
# response = g4f.ChatCompletion.create(
#     model=g4f.models.gpt_4,
#     messages=[{"role": "user", "content": "Hello"}],
# )  # Alternative model setting

# print(response)

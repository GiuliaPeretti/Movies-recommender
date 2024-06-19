import gradio as gr
import pandas as pd
def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distances=sorted(list(enumerate(similarity.iloc[index-1])), reverse=True, key = lambda x: x[1])
    result=""
    c=1
    for i in distances[1:6]:
        result = result + str(c) + ") " + movies.iloc[i[0]].title + "\n" 
        c+=1
    return(result)


similarity=pd.read_csv("similarity.csv")
movies=pd.read_csv("tmdb_5000_movies.csv")
titles=movies['original_title'].tolist()

with gr.Blocks() as demo:
    gr.Markdown("Choose a movie you liked:")
    inp=gr.Dropdown(titles)
    btn = gr.Button("Run")
    gr.Markdown("Movies recommended:")
    out=gr.TextArea()
    btn.click(fn=recommend, inputs=inp, outputs=out)

demo.launch(share=False)
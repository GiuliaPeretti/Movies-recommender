import gradio as gr
import pandas as pd
def recommend(movie):
    print(movie)
    index=movies[movies['title']==movie].index[0]
    print(index)
    print(similarity.iloc[[index]])
    distances=sorted(list(enumerate(similarity.iloc[index-1])), reverse=True, key = lambda x: x[1])
    result=[]
    for i in distances[1:6]:
        result.append(movies.iloc[i[0]].title)
    return(str(result))


similarity=pd.read_csv("similarity.csv")
movies=pd.read_csv("tmdb_5000_movies.csv")
titles=movies['original_title'].tolist()

with gr.Blocks() as demo:
    gr.Markdown("Start typing below and then click **Run** to see the output.")
    inp=gr.Dropdown(titles)
    btn = gr.Button("Run")
    out=gr.TextArea()
    btn.click(fn=recommend, inputs=inp, outputs=out)

demo.launch(share=False)
# Core Pkgs
import streamlit as st
import streamlit.components.v1 as stc

# EDA Pkgs
import pandas as pd
import neattext.functions as nfx
import random


# Data Viz Pkgs
import matplotlib

matplotlib.use("Agg")
import altair as alt

# Utils
@st.cache
def load_bible(data):
    df = pd.read_csv(data)
    return df


from utils import (
    HTML_BANNER,
    HTML_RANDOM_TEMPLATE,
    render_entities,
    get_tags,
    mytag_visualizer,
    plot_mendelhall_curve,
    plot_word_freq_with_altair,
    get_most_common_tokens,
)


def main():
    stc.html(HTML_BANNER)
    menu = ["Home", "MultiVerse", "About"]

    df = load_bible("data/KJV_Bible.csv")

    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Single Verse Search")
        book_list = df["book"].unique().tolist()
        book_name = st.sidebar.selectbox("Book", book_list)
        chapter = st.sidebar.number_input("Chapter", 1)
        verse = st.sidebar.number_input("Verse", 1)
        bible_df = df[df["book"] == book_name]

        # Layout
        c1, c2 = st.beta_columns([2, 1])

        # Single Verse Layout
        with c1:

            try:
                selected_passage = bible_df[
                    (bible_df["chapter"] == chapter) & (bible_df["verse"] == verse)
                ]
                passage_details = "{} Chapter::{} Verse::{}".format(
                    book_name, chapter, verse
                )
                st.info(passage_details)
                passage = "{}".format(selected_passage["text"].values[0])
                st.write(passage)

            except:
                st.warning("Book out of Range")

        with c2:
            # st.success("Verse of the Day")
            chapter_list = range(10)
            verse_list = range(20)
            ch_choice = random.choice(chapter_list)
            vs_choice = random.choice(verse_list)
            random_book_name = random.choice(book_list)

            # st.write("Book:{},Ch:{},Vs:{}".format(random_book_name,ch_choice,vs_choice))
            rand_bible_df = df[df["book"] == random_book_name]

            try:
                randomly_selected_passage = rand_bible_df[
                    (rand_bible_df["chapter"] == ch_choice)
                    & (rand_bible_df["verse"] == vs_choice)
                ]
                mytext = randomly_selected_passage["text"].values[0]
            except:
                mytext = rand_bible_df[
                    (rand_bible_df["chapter"] == 1) & (rand_bible_df["verse"] == 1)
                ]["text"].values[0]

            stc.html(HTML_RANDOM_TEMPLATE.format(mytext), height=300)

        # Search Topic/Term
        search_term = st.text_input("Term/Topic")
        with st.beta_expander("View Results"):
            retrieved_df = df[df["text"].str.contains(search_term)]
            st.dataframe(retrieved_df[["book", "chapter", "verse", "text"]])

    elif choice == "MultiVerse":
        st.subheader("MultiVerse Retrieval")
        book_list = df["book"].unique().tolist()
        book_name = st.sidebar.selectbox("Book", book_list)
        chapter = st.sidebar.number_input("Chapter", 1)
        bible_df = df[df["book"] == book_name]
        all_verse = bible_df["verse"].unique().tolist()
        verse = st.sidebar.multiselect("Verse", all_verse, default=1)
        selected_passage = bible_df.iloc[verse]
        st.dataframe(selected_passage)
        passage_details = "{} Chapter::{} Verse::{}".format(book_name, chapter, verse)
        st.info(passage_details)

        # Layout
        col1, col2 = st.beta_columns(2)
        # Join all text as a sentence
        docx = " ".join(selected_passage["text"].tolist())

        with col1:
            st.info("Details")
            for i, row in selected_passage.iterrows():
                st.write(row["text"])

        with col2:
            st.success("StudyMode")
            with st.beta_expander("Visualize Entities"):
                # st.write(docx)
                render_entities(docx)

            with st.beta_expander("Visualize Pos Tags"):
                tagged_docx = get_tags(docx)
                processed_tags = mytag_visualizer(tagged_docx)
                # st.write(processed_tags)# Raw
                stc.html(processed_tags, height=1000, scrolling=True)

            with st.beta_expander("Keywords"):
                processed_docx = nfx.remove_stopwords(docx)
                keywords_tokens = get_most_common_tokens(processed_docx, 5)
                st.write(keywords_tokens)

            with st.beta_expander("Pos Tags Plot"):
                tagged_docx = get_tags(docx)
                tagged_df = pd.DataFrame(tagged_docx, columns=["Tokens", "Tags"])
                # st.dataframe(tagged_df)
                df_tag_count = tagged_df["Tags"].value_counts().to_frame("counts")
                df_tag_count["tag_type"] = df_tag_count.index
                # st.dataframe(df_tag_count)

                c = alt.Chart(df_tag_count).mark_bar().encode(x="tag_type", y="counts")
                st.altair_chart(c, use_container_width=True)

        with st.beta_expander("Verse Curve"):
            plot_mendelhall_curve(docx)

        with st.beta_expander("Word Freq Plot"):
            plot_word_freq_with_altair(docx)

    else:
        st.subheader("About")
        st.text("Build with Streamlit")
        st.text("Jesse E.Agbe(JCharis)")
        st.success("Jesus Saves @JCharisTech")


if __name__ == "__main__":
    main()

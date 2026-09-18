from src.states.blogstate import BlogState
from langchain_core.messages import HumanMessage, SystemMessage
from src.states.blogstate import Blog

class BlogNode:
    """
    A class to represent the blog node
    """
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state:BlogState):
        """
        create the title for the blog
        """

        if "topic" in state and state["topic"]:
            prompt = """
                    You are an expert blog content writer. Use markdown formatting. Generate a
                    blog title for the {topic}. This title should be creative and SEO friendly.
                    """
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)

            return {"blog":{"title":response.content}}

    def content_generation(self, state:BlogState):
        """
        create a content based on the title.
        """
        if "topic" in state and state["topic"]:
            prompt = """
                    You are an expert blog content writer. Use markdown formatting. Generate a
                    blog detailed blog content with the detailed break down for the {topic}.
                    """
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)

            return {"blog":{"title":state['blog']['title'], "content":response.content}}

    def translation(self, state:BlogState):
        """
        Translate the content to the specified language
        """
        translation_prompt = """
        Translate the following content into {current_language}.
        - Maintain the original tone, style and formatting
        - Adapt cultural references and idioms to be appropriate for {current_language}.
        ORIGINAL_TITLE:
        {blog_title}
        ORINGINAL_CONTENT:
        {blog_content}
        """
        blog_content = state["blog"]["content"]
        blog_title = state["blog"]["title"]
        messages = [
            HumanMessage(translation_prompt.format(current_language=state["current_language"], blog_title=blog_title, blog_content=blog_content))
        ]
        # translation_content = self.llm.with_structured_output(Blog).invoke(messages)
        translation_content = self.llm.invoke(messages)

        return {"blog": {"title":blog_title, "content": translation_content}}

    def route(self, state:BlogState):
        return {"current_language": state["current_language"]}

    def route_decision(self, state:BlogState):
        """
        Route the content to the respective translation function.
        """
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french":
            return "french"
        else:
            return state["current_language"]


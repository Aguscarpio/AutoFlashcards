import os
from pdf_handler import PDFHandler
from highlight_context_extractor import HighlightContextExtractor
from flashcard_generator import (
    FlashcardGenerator,
    OpenAIProvider,
    AnthropicProvider,
    GeminiProvider,
)
from flashcard_output_to_anki_handler import FlashcardOutputHandler
from dotenv import load_dotenv


def get_llm_provider(provider_name: str, api_key: str):
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider,
    }
    if provider_name not in providers:
        raise ValueError(
            f"Unsupported provider: {provider_name}\n\nThe options are: \n{providers}"
        )
    return providers[provider_name](api_key)


def main():
    load_dotenv()

    pdf_path = "sample_01.pdf"
    pdf_handler = PDFHandler(pdf_path)
    highlights = pdf_handler.extract_highlights()

    context_extractor = HighlightContextExtractor(pdf_handler)
    contexts = context_extractor.get_contexts(highlights)

    # Safely get API key and provider name from .env variables
    api_key = os.getenv("API_KEY")
    provider_name = os.getenv("LLM_PROVIDER")

    # Create the appropiate LLMProvider instance
    llm_provider = get_llm_provider(provider_name, api_key)

    flashcard_generator = FlashcardGenerator(llm_provider)
    flashcards = flashcard_generator.generate_flashcards(contexts)

    output_handler = FlashcardOutputHandler()
    output_handler.save_to_txt(flashcards, "output_flashcards.txt")
    output_handler.create_anki_deck(flashcards, "My Flashcards")


if __name__ == "__main__":
    main()

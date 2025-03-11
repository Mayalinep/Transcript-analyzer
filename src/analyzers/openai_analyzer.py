import logging
from typing import Dict, Optional
from .base import TextAnalyzer
from .basic_analyzer import BasicAnalyzer

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class OpenAIAnalyzer(TextAnalyzer):
    """Analyseur de texte utilisant OpenAI"""
    
    def __init__(self, api_key: Optional[str] = None):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package is not installed. Install it with 'pip install openai'")
        if not api_key:
            raise ValueError("An OpenAI API key is required to use this analyzer.")
        
        logging.info("Initializing OpenAI analyzer...")
        self.client = openai.OpenAI(api_key=api_key)
        try:
            # Test API key
            self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Connection test"}, {"role": "user", "content": "Test"}],
                max_tokens=5
            )
            logging.info("OpenAI connection established successfully")
        except Exception as e:
            logging.error(f"Error initializing OpenAI: {str(e)}")
            raise ValueError(f"Could not initialize OpenAI: {str(e)}")

    def clean_text(self, text: str) -> str:
        """Clean text using GPT."""
        try:
            logging.info("Cleaning text with OpenAI...")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a text correction expert. Clean this text by: 1) Correcting grammar and spelling, 2) Improving punctuation, 3) Removing unnecessary repetitions."},
                    {"role": "user", "content": text}
                ]
            )
            cleaned_text = response.choices[0].message.content
            logging.info("Text cleaned successfully")
            return cleaned_text
        except Exception as e:
            logging.error(f"Error cleaning text with OpenAI: {str(e)}")
            return BasicAnalyzer().clean_text(text)

    def create_summary(self, text: str, max_length: int = 1500) -> str:
        """Create summary using GPT."""
        try:
            logging.info("Creating summary with OpenAI...")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are a content synthesis expert. Create a structured summary by:
1) Identifying 3-4 main key points
2) Explaining important concepts
3) Highlighting relationships between different parts
4) Using structure markers (First, Then, Finally, etc.)"""},
                    {"role": "user", "content": text}
                ],
                max_tokens=500
            )
            summary = response.choices[0].message.content
            logging.info("Summary created successfully")
            return summary
        except Exception as e:
            logging.error(f"Error generating summary with OpenAI: {str(e)}")
            return BasicAnalyzer().create_summary(text, max_length)

    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract sections using GPT."""
        try:
            logging.info("Extracting sections with OpenAI...")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are a content organization expert. Analyze this text and organize it into coherent sections.
For each section:
1) Identify key concepts and main ideas
2) Organize content logically
3) Add relevant subtitles if needed
4) Ensure smooth transitions between sections

Main sections should be:
- Introduction (context and objectives)
- Installation and Configuration (technical steps)
- Features (capabilities and characteristics)
- Usage (concrete examples and use cases)
- Conclusion (synthesis and perspectives)"""},
                    {"role": "user", "content": text}
                ],
                max_tokens=1500
            )
            
            sections_text = response.choices[0].message.content
            sections = {
                "Introduction": "",
                "Installation and Configuration": "",
                "Features": "",
                "Usage": "",
                "Conclusion": ""
            }
            
            current_section = "Introduction"
            current_content = []
            
            for line in sections_text.split('\n'):
                section_match = None
                for section_name in sections.keys():
                    if section_name.upper() in line.upper():
                        section_match = section_name
                        break
                
                if section_match:
                    if current_content:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = section_match
                    current_content = []
                else:
                    current_content.append(line)
            
            if current_content:
                sections[current_section] = '\n'.join(current_content)
            
            # Second pass to improve each section
            logging.info("Improving sections...")
            for section_name, content in sections.items():
                if content.strip():
                    try:
                        response = self.client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": f"""Improve this '{section_name}' section by:
1) Adding bullet points for important points
2) Making key concepts bold
3) Structuring content clearly
4) Adding examples if relevant"""},
                                {"role": "user", "content": content}
                            ],
                            max_tokens=500
                        )
                        sections[section_name] = response.choices[0].message.content
                        logging.info(f"Section '{section_name}' improved successfully")
                    except Exception as e:
                        logging.error(f"Error improving section '{section_name}': {str(e)}")
            
            logging.info("Sections extraction completed successfully")
            return sections
            
        except Exception as e:
            logging.error(f"Error extracting sections with OpenAI: {str(e)}")
            return BasicAnalyzer().extract_sections(text) 
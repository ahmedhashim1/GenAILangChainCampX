from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal
from pydantic import BaseModel, EmailStr, Field

load_dotenv()

model = ChatOpenAI()


# Schema

class Review(BaseModel):
    key_themes: list[str] = Field(description="Write down all the key features discuss in the review in list")
    summary: str = Field(description="A brief summary of the review.")
    sentiment: Literal["neutral", "positive", "negative"] = Field(
        description="Return sentiment for the review, either positive, negative, or neutral.")
    score: float = Field(description="Return score for the review between 1-5 (1 is worse and 5 is the best).")
    pros: Optional[list[str]] = Field(default=None, description="Write down pros from the review in list")
    cons: Optional[list[str]] = Field(default=None, description="Write down cons from the review in list")
    review_name: str = Field(description="The name of the reviewer, if available.")


struct_model = model.with_structured_output(Review)

result = struct_model.invoke("""The Samsung Galaxy S24 Ultra has been universally acclaimed by tech publications (PCMag, GSMArena, Android Authority, TechRadar) as the most powerful and feature-complete Android flagship available. While it looks similar to its predecessor, its key upgrades—particularly the performance boost, the new anti-reflective display, and the massive focus on Galaxy AI—cement its status as the top-tier "Ultra" device.
Core Upgrades and Experience
The device features a premium titanium frame for improved durability and the exclusive Snapdragon 8 Gen 3 for Galaxy processor, which reviewers noted delivers blazing-fast performance, especially for demanding games and running the new on-device AI features.
The 6.8-inch Dynamic AMOLED 2X display is a major highlight. It’s brighter than before (up to 2,600 nits) and features the new Gorilla Armor glass, which drastically reduces glare and reflections, making the screen exceptionally readable in bright sunlight—a feature praised as a significant real-world improvement. The screen is also now perfectly flat, which reviewers noted enhances the experience of using the built-in S Pen.
The camera system remains one of the most versatile in the market. The high-resolution 200MP main camera and the 3x telephoto are excellent, while the major change is the replacement of the 10x optical zoom with a 50MP 5x optical zoom. Reviewers generally agree this was a smart move, as the new setup delivers sharper, more practical shots at 5x while using AI and the high-res sensor to maintain excellent quality at 10x and beyond.

Key Pros and Cons

The overall consensus is that the S24 Ultra is a superb phone, but its value proposition is best for power users and those who use the S Pen or camera zoom features frequently.

    Pros:
        Leading Performance: Blazing fast speed thanks to the optimized Snapdragon 8 Gen 3 for Galaxy chipset.
        Incredible Display: Brightness and the revolutionary anti-reflective Gorilla Armor glass make it the best display for outdoor use.
        Galaxy AI Suite: Features like Circle to Search, Live Translate (for calls), and AI photo editing add genuinely useful capabilities.
        Long-Term Support: Class-leading promise of 7 years of OS and security updates for extended device life.
        S Pen Integration: Remains the only Android flagship with a built-in, no-latency stylus for ultimate productivity.
        Versatile Camera: The new 5x 50MP telephoto provides superior clarity at that focal length, and overall image processing is improved with more natural colors.

    Cons:
        High Cost: It is one of the most expensive non-folding smartphones on the market.
        Slow Charging: The 45W wired charging is significantly slower compared to many non-Apple/Pixel rivals.
        Incremental Upgrade: Owners of the S23 Ultra may not find the hardware changes substantial enough to justify an immediate upgrade.
        AI Feature Disclaimer: The free status of the new Galaxy AI features is only guaranteed until the end of 2025.
        Bulk: Despite the titanium frame, it remains a large, heavy phone that won't appeal to users seeking a compact device.

    Review by Ahmed Hashim        
        """)

# print(result)
print("The result received:", result.summary)
print("Sentiment:", result.sentiment)
print("Score:", result.score)
print("Key themes:", result.key_themes)
print("Pros:", result.pros)
print("Cons:", result.cons)
print("Reviewd by:", result.review_name)

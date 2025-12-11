import os
import json
import csv
import pandas as pd
from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from collections import defaultdict

# --- Configuration and Initialization ---
# NOTE: Replace with your actual API key or set as environment variable.
if not os.environ.get("OPENAI_API_KEY"):
    print("WARNING: OPENAI_API_KEY not found. Please set the environment variable.")
    # In a real environment, we would raise an error here.

# Initialize the LLM (using GPT-4o for robust structured extraction)
llm = ChatOpenAI(model="gpt-4o", temperature=0.0)


# --- 1. Define the Structured Output Schema for Unit Number Extraction ---
class ExtractedUnitData(BaseModel):
    """Schema for extracting the critical Unit Number and confidence."""
    unit_number: str = Field(description="The unique 'Unit Number' found on the invoice.")
    confidence_score: float = Field(
        description="The LLM's confidence (0.0 to 1.0) in the accuracy of the extracted unit_number.")
    evidence_text: str = Field(description="A short snippet of text surrounding the Unit Number to provide evidence.")


parser = JsonOutputParser(pydantic_object=ExtractedUnitData)


# --- 2. Define the Extraction Chain (LangChain Pipeline) ---
def create_unit_extraction_chain(llm_model):
    """
    Creates a LangChain pipeline for high-accuracy Unit Number extraction.
    """
    system_message = (
        "You are a hyper-focused document auditing agent. Your sole task is to find the "
        "unique 'Unit Number' from the provided invoice text. You must output the result "
        "STRICTLY as the required JSON schema, along with your confidence and text evidence. "
        "If the Unit Number is not found, use an empty string for the unit_number and 0.0 confidence."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "Extract the Unit Number from the following invoice OCR text:\n\n{ocr_text}"),
        ("human", "Your output MUST be a JSON object that strictly follows this schema:\n{format_instructions}"),
    ])

    return prompt | llm_model | parser


# --- 3. Mock OCR Data Source (Simulating the Document AI step) ---
def get_mock_ocr_data(count=100) -> List[dict]:
    """
    Simulates loading OCR text for N documents.
    In a real system, this would call Azure/Google Document AI.
    """
    data = []
    # Create N unique filenames
    filenames = [f"invoice_{i:04d}.pdf" for i in range(count)]

    # Generate 5 unit numbers that are deliberately duplicates
    duplicate_units = ["UNIT-A101", "UNIT-B202", "UNIT-C303", "UNIT-D404", "UNIT-E505"] * (count // 20)

    for i in range(count):
        filename = filenames[i]
        unit_number = duplicate_units.pop(0) if duplicate_units else f"UNIT-{i + 1000}"

        # Simulate raw OCR text content
        ocr_text = f"Shipment ID: 998234. Invoice Date: 2025-10-01. Customer Ref: XZY-77. Unique Unit Number: {unit_number}. Total: $450.00."

        data.append({
            "filename": filename,
            "ocr_text": ocr_text
        })
    return data


# --- 4. Main Processing and Duplication Reporting ---
def run_pilot_extraction(ocr_data: List[dict]):
    """
    Runs the extraction chain across all mock OCR data and generates the audit report.
    """
    audit_results = []
    unit_counts = defaultdict(list)
    extraction_chain = create_unit_extraction_chain(llm)

    print("--- Phase 1: Running Pilot Extraction (Simulated) ---")

    for doc in ocr_data:
        filename = doc["filename"]
        ocr_text = doc["ocr_text"]

        # Invoke the chain for structured extraction
        try:
            extracted_data = extraction_chain.invoke({
                "ocr_text": ocr_text,
                "format_instructions": parser.get_format_instructions()
            })

            # Pydantic validation is handled by the parser, but we ensure structure
            validated_data = ExtractedUnitData.model_validate(extracted_data)

            unit = validated_data.unit_number.strip()
            confidence = validated_data.confidence_score
            evidence = validated_data.evidence_text

            # Store result
            audit_results.append({
                "filename": filename,
                "unit_number": unit,
                "confidence": confidence,
                "evidence": evidence
            })

            # Track unit number occurrences for duplicate report
            if unit:
                unit_counts[unit].append(filename)

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            audit_results.append({
                "filename": filename,
                "unit_number": "ERROR",
                "confidence": 0.0,
                "evidence": str(e)
            })

    # Convert results to DataFrame for easy export and analysis
    df_results = pd.DataFrame(audit_results)

    # 1. Output Main CSV/Excel
    main_output_file = "phase1_extraction_report.csv"
    df_results.to_csv(main_output_file, index=False)
    print(f"\n[DONE] Main Extraction Report saved to: {main_output_file}")

    # 2. Duplicate Report Generation
    duplicate_units_data = [
        {"unit_number": unit, "occurrence_count": len(files), "associated_filenames": ", ".join(files)}
        for unit, files in unit_counts.items() if len(files) >= 2
    ]

    df_duplicates = pd.DataFrame(duplicate_units_data)
    duplicate_output_file = "phase1_duplicate_unit_report.csv"
    df_duplicates.to_csv(duplicate_output_file, index=False)
    print(f"[DONE] Duplicate Unit Report saved to: {duplicate_output_file}")

    # 3. Accuracy Calculation (Simulated check)
    # Since mock data is perfectly structured, accuracy should be near 100%
    # in a real run, this would be against human-verified ground truth data.
    successful_extractions = df_results[df_results['unit_number'] != 'ERROR'].shape[0]
    target_accuracy = 98.0
    print(f"\n--- Pilot Summary ---")
    print(f"Total processed documents: {len(ocr_data)}")
    print(f"Successful extractions: {successful_extractions}")
    print(f"Accuracy (Simulated): {successful_extractions / len(ocr_data) * 100:.2f}% (Target: {target_accuracy}%)")


if __name__ == "__main__":
    # Simulate processing 100 documents for the pilot phase
    pilot_data = get_mock_ocr_data(count=100)
    run_pilot_extraction(pilot_data)

    # The structure for Phase 3 (Excel Audit Engine) is in the next file.

import pandas as pd
import logging
import re
import os
from typing import List, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='csv_parser.log'
)

class PhoneNumberNormalizer:
    @staticmethod
    def normalize_phone(phone: str) -> Optional[str]:
        """Normalize phone number format, return None if invalid"""
        if not isinstance(phone, str):
            return None
        
        # Remove all non-numeric characters
        digits = re.sub(r'\D', '', phone)
        
        # Check if we have a valid number of digits (10 or 11)
        if len(digits) == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
        return None

class CSVParser:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.phone_normalizer = PhoneNumberNormalizer()
        
    def validate_phone_columns(self, row: pd.Series, phone_columns: List[str]) -> Optional[str]:
        """Check multiple phone columns for valid number"""
        for col in phone_columns:
            if pd.notna(row[col]):
                normalized = self.phone_normalizer.normalize_phone(str(row[col]))
                if normalized:
                    return normalized
        return None

    def process_csv(self):
        try:
            # Read input CSV
            logging.info(f"Reading input file: {self.input_file}")
            df = pd.read_csv(self.input_file)
            
            # Identify phone number columns
            phone_columns = [col for col in df.columns if 'phone' in col.lower()]
            
            # Create normalized phone numbers
            df['normalized_phone'] = df.apply(
                lambda row: self.validate_phone_columns(row, phone_columns), 
                axis=1
            )
            
            # Remove duplicates based on normalized phone
            df_cleaned = df.drop_duplicates(subset=['normalized_phone'])
            
            # Create TextyPro template format
            texty_pro_df = pd.DataFrame({
                'Phone': df_cleaned['normalized_phone'],
                # Add other required TextyPro columns here
            })
            
            # Remove rows with invalid phone numbers
            texty_pro_df = texty_pro_df.dropna(subset=['Phone'])
            
            # Save to output CSV
            texty_pro_df.to_csv(self.output_file, index=False)
            logging.info(f"Successfully wrote output file: {self.output_file}")
            
        except FileNotFoundError:
            logging.error(f"Input file not found: {self.input_file}")
            raise
        except pd.errors.EmptyDataError:
            logging.error("Input CSV file is empty")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise

def main():
    try:
        input_file = "input.csv"  # Replace with your input file path
        output_file = "output.csv"  # Replace with your output file path
        
        parser = CSVParser(input_file, output_file)
        parser.process_csv()
        
    except Exception as e:
        logging.error(f"Failed to process CSV: {str(e)}")
        raise

if __name__ == "__main__":
    main()

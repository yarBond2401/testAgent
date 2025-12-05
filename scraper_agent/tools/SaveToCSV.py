import csv
import os
from datetime import datetime
from typing import List
from agency_swarm.tools import BaseTool
from pydantic import Field


# Get project root directory (where agency.py is located)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Output directory for CSV files - mnt folder at repository root level
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "mnt")


class SaveToCSV(BaseTool):
    """
    Saves comprehensive company intelligence data to a CSV file.
    Data is sorted by suitability score (from highest to lowest).
    Creates the mnt directory if it doesn't exist.
    Returns the absolute file path where the CSV was saved.
    """
    
    companies: List[dict] = Field(
        ...,
        description="""List of company dictionaries. Each dictionary should contain:
        - company_name: str - Name of the company
        - website: str - Company website URL
        - phone: str - Phone number ("Not available" if not found)
        - description: str - 1-2 sentence description of what the company does
        - funding_info: str - Funding stage, year, amount, investors
        - valuation: str - Company valuation or estimated range
        - early_story: str - How the company started, key pivots
        - reddit_feedback: str - Summary of Reddit discussions (positive, negative, pain points)
        - profitability_info: str - Revenue, growth, unit economics
        - proposal: str - Tailored business proposal
        - suitability_score: int - Score from 0-100 (Business Opportunity Score)"""
    )
    
    filename_prefix: str = Field(
        default="company_intelligence",
        description="Prefix for the output CSV filename. The full filename will be: {prefix}_{timestamp}.csv"
    )

    def run(self):
        """
        Saves the company intelligence data to a CSV file sorted by suitability score.
        Returns the absolute path to the created CSV file.
        """
        # Step 1: Ensure mnt directory exists at repository root
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Step 2: Sort companies by suitability_score (highest first)
        sorted_companies = sorted(
            self.companies,
            key=lambda x: x.get("suitability_score", 0),
            reverse=True
        )
        
        # Step 3: Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.filename_prefix}_{timestamp}.csv"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Step 4: Define CSV headers
        headers = [
            "Rank",
            "Company",
            "Website",
            "Phone",
            "Description",
            "Funding",
            "Valuation",
            "Early Story",
            "Reddit Feedback",
            "Profitability",
            "Business Proposal",
            "Score"
        ]
        
        # Step 5: Write data to CSV
        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            for rank, company in enumerate(sorted_companies, start=1):
                row = [
                    rank,
                    company.get("company_name", "N/A"),
                    company.get("website", "N/A"),
                    company.get("phone", "Not available"),
                    company.get("description", "N/A"),
                    company.get("funding_info", "No public funding data found"),
                    company.get("valuation", "N/A"),
                    company.get("early_story", "N/A"),
                    company.get("reddit_feedback", "No significant Reddit discussions found"),
                    company.get("profitability_info", "Not publicly available"),
                    company.get("proposal", "N/A"),
                    company.get("suitability_score", 0)
                ]
                writer.writerow(row)
        
        # Step 6: Generate CSV row strings for output
        csv_rows = []
        for company in sorted_companies:
            csv_row = f"{company.get('company_name', 'N/A')}, {company.get('website', 'N/A')}, {company.get('phone', 'Not available')}, {company.get('funding_info', 'N/A')}, {company.get('valuation', 'N/A')}, {company.get('early_story', 'N/A')[:50]}..., {company.get('reddit_feedback', 'N/A')[:50]}..., {company.get('profitability_info', 'N/A')[:50]}..., {company.get('proposal', 'N/A')[:50]}..., {company.get('suitability_score', 0)}"
            csv_rows.append(f"CSV_ROW: {csv_row}")
        
        # Step 7: Return the file path and summary
        absolute_path = os.path.abspath(filepath)
        
        result = f"""✅ CSV file saved successfully!

📁 File Path: {absolute_path}
📊 Total Companies: {len(sorted_companies)}

🏆 Top 3 Companies by Score:
"""
        for i, company in enumerate(sorted_companies[:3], 1):
            result += f"{i}. {company.get('company_name', 'N/A')} (Score: {company.get('suitability_score', 0)}/100)\n"
        
        result += f"\n{chr(10).join(csv_rows[:3])}"
        
        return result


if __name__ == "__main__":
    # Test case with comprehensive sample data
    test_companies = [
        {
            "company_name": "Parker",
            "website": "https://parker.com",
            "phone": "+1-555-123-4567",
            "description": "Parker offers corporate cards and spend management for ecommerce businesses.",
            "funding_info": "Stage: Series B, Year: 2023, Amount: $50M, Investors: Valar Ventures, Founders Fund",
            "valuation": "$250M (post-money)",
            "early_story": "Founded in 2019 by ex-Stripe engineers. Started as expense tracking tool, pivoted to corporate cards after seeing demand from ecommerce clients.",
            "reddit_feedback": "Positive: Fast approval, good limits | Negative: Customer support slow | Pain points: Integration issues with some accounting software",
            "profitability_info": "ARR: ~$15M (estimated), Growth: 150% YoY, Unit economics: Improving",
            "proposal": "Offer API integration partnership for seamless expense categorization. Provide analytics dashboard for spend insights. Help with international expansion.",
            "suitability_score": 85
        },
        {
            "company_name": "Ramp",
            "website": "https://ramp.com",
            "phone": "+1-555-987-6543",
            "description": "Ramp is a corporate card and spend management platform focused on helping businesses save money.",
            "funding_info": "Stage: Series D, Year: 2024, Amount: $300M, Investors: Founders Fund, Stripe, Goldman Sachs",
            "valuation": "$8.1B",
            "early_story": "Founded in 2019. Differentiated by focusing on cost savings rather than rewards. Rapid growth during pandemic as businesses sought to cut costs.",
            "reddit_feedback": "Positive: Great UI, real savings | Negative: Limited international support | Pain points: Restrictions on some merchant categories",
            "profitability_info": "ARR: $100M+, Growth: 100% YoY, Path to profitability: 2025",
            "proposal": "Strategic partnership for SMB market expansion. Co-branded expense analytics. Integration with our payment rails.",
            "suitability_score": 72
        },
        {
            "company_name": "Brex",
            "website": "https://brex.com",
            "phone": "Not available",
            "description": "Brex provides corporate cards, expense management, and banking services for startups and enterprises.",
            "funding_info": "Stage: Series D, Year: 2022, Amount: $300M, Investors: Tiger Global, Y Combinator, Greenoaks",
            "valuation": "$12.3B (2022), down-round to ~$6B (2024)",
            "early_story": "Founded in 2017 by Brazilian founders who previously built a payments company. Initially focused on startups, expanded to enterprises.",
            "reddit_feedback": "Positive: High limits for startups | Negative: Dropped SMB customers in 2022 | Pain points: Account closures without warning",
            "profitability_info": "ARR: $200M+ (estimated), Growth: Slowing, Focus on enterprise",
            "proposal": "Target their churned SMB customers. Offer migration tools. Position as more stable alternative for growth-stage companies.",
            "suitability_score": 65
        }
    ]
    
    tool = SaveToCSV(companies=test_companies, filename_prefix="test_intelligence")
    print(tool.run())

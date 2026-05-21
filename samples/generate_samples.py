"""
Generate sample Loan Agreement and ESG Report PDFs for demo purposes.
Run this script to create the sample files in the samples/ directory.
"""
import os
from fpdf import FPDF


class SamplePDFGenerator:
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_loan_agreement(self):
        """Generate a realistic green loan agreement with ESG covenants."""
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Page 1 - Title & Overview
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 20)
        pdf.cell(0, 15, "GREEN LOAN AGREEMENT", ln=True, align="C")
        pdf.ln(5)
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 8, "Sustainability-Linked Loan Facility Agreement", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "PARTIES", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "Lender: Global Sustainable Finance Bank (GSFB)\n"
            "Borrower: TechCorp Industries Ltd.\n"
            "Facility Amount: USD 250,000,000\n"
            "Tenor: 5 Years (2023-2028)\n"
            "Effective Date: January 1, 2023\n"
            "Maturity Date: December 31, 2028"
        ))
        pdf.ln(5)

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "1. PURPOSE", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "This Green Loan Agreement is entered into for the purpose of financing "
            "environmentally sustainable projects and operations of the Borrower, in "
            "alignment with the Green Loan Principles (GLP) 2023 published by the Loan "
            "Market Association (LMA). The Borrower commits to deploying the proceeds "
            "towards eligible green projects including renewable energy installations, "
            "energy efficiency upgrades, and emissions reduction initiatives."
        ))
        pdf.ln(5)

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "2. DEFINITIONS", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "2.1 'ESG KPIs' means the Environmental, Social, and Governance Key Performance "
            "Indicators as defined in Schedule A of this Agreement.\n\n"
            "2.2 'Baseline Year' refers to the Financial Year 2023 (FY2023) against which "
            "all performance targets shall be measured.\n\n"
            "2.3 'Reporting Period' means each Financial Year during the Tenor of this Agreement.\n\n"
            "2.4 'Sustainability Report' means the annual ESG/Sustainability Report prepared "
            "by the Borrower in accordance with GRI Standards or SASB Standards.\n\n"
            "2.5 'Scope 1 Emissions' means direct GHG emissions from owned or controlled sources.\n\n"
            "2.6 'Scope 2 Emissions' means indirect GHG emissions from the generation of "
            "purchased energy consumed by the Borrower.\n\n"
            "2.7 'Scope 3 Emissions' means all other indirect GHG emissions in the Borrower's value chain."
        ))

        # Page 2 - ESG Covenants
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, "SCHEDULE A: ESG COVENANTS", ln=True, align="C")
        pdf.ln(5)

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "3. ENVIRONMENTAL COVENANTS", ln=True)
        pdf.ln(3)

        # Covenant 1
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Covenant 3.1: Scope 2 GHG Emissions Reduction", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "The Borrower shall achieve a reduction in Scope 2 Greenhouse Gas (GHG) "
            "emissions of at least 15% by the end of Financial Year 2026 (FY2026), "
            "measured against the FY2023 baseline of 45,000 tonnes CO2 equivalent (tCO2e). "
            "This translates to a maximum permissible Scope 2 emission level of 38,250 tCO2e "
            "by FY2026. The Borrower shall report Scope 2 emissions annually using the "
            "market-based method in accordance with the GHG Protocol Corporate Standard."
        ))
        pdf.ln(5)

        # Covenant 2
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Covenant 3.2: Renewable Energy Adoption", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "The Borrower shall ensure that renewable energy sources constitute at least "
            "30% of total energy consumption by the end of FY2026. The baseline renewable "
            "energy share as of FY2023 is 18%. Eligible renewable energy sources include "
            "solar photovoltaic, wind power, hydroelectric power, and biomass energy. "
            "The Borrower may count purchased Renewable Energy Certificates (RECs) and "
            "Power Purchase Agreements (PPAs) towards this target."
        ))
        pdf.ln(5)

        # Covenant 3
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Covenant 3.3: Energy Efficiency Improvement", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "The Borrower shall achieve a minimum 10% improvement in energy intensity "
            "(measured as MWh per million USD revenue) by FY2026, compared to the FY2023 "
            "baseline of 85 MWh per million USD revenue. The target energy intensity shall "
            "not exceed 76.5 MWh per million USD revenue by FY2026."
        ))
        pdf.ln(5)

        # Covenant 4
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Covenant 3.4: Water Usage Reduction", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "The Borrower shall reduce total water withdrawal by at least 20% by FY2026, "
            "measured against the FY2023 baseline of 500,000 cubic meters (m3). The maximum "
            "permissible water withdrawal shall be 400,000 m3 by FY2026. Water recycling "
            "and rainwater harvesting volumes may be credited towards this target."
        ))
        pdf.ln(5)

        # Covenant 5
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Covenant 3.5: Waste Diversion Rate", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "The Borrower shall achieve a waste diversion rate (waste diverted from "
            "landfill as a percentage of total waste generated) of at least 75% by FY2026. "
            "The FY2023 baseline waste diversion rate is 60%. Acceptable diversion methods "
            "include recycling, composting, and waste-to-energy conversion."
        ))

        # Page 3 - Reporting & Compliance
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "4. REPORTING REQUIREMENTS", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "4.1 The Borrower shall submit an annual Sustainability Report within 120 days "
            "of each Financial Year end.\n\n"
            "4.2 The report shall follow GRI Standards (Core or Comprehensive option) or "
            "SASB Standards applicable to the Borrower's industry.\n\n"
            "4.3 All ESG KPIs shall be reported with:\n"
            "   (a) Current year values\n"
            "   (b) Prior year comparative values\n"
            "   (c) Baseline year values\n"
            "   (d) Methodology and assumptions used\n\n"
            "4.4 The Borrower shall obtain third-party limited assurance on material ESG "
            "KPIs from an independent verification body."
        ))
        pdf.ln(5)

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "5. COMPLIANCE AND CONSEQUENCES", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "5.1 Failure to meet any ESG covenant shall constitute a Sustainability Event, "
            "triggering a review period of 90 days.\n\n"
            "5.2 During the review period, the Borrower shall submit a corrective action plan.\n\n"
            "5.3 If remediation is not achieved within the review period, the interest rate "
            "shall increase by 25 basis points per failed covenant, up to a maximum of "
            "75 basis points.\n\n"
            "5.4 Persistent non-compliance (two consecutive years of failure on the same "
            "covenant) may constitute an Event of Default under Section 8 of this Agreement."
        ))

        path = os.path.join(self.output_dir, "sample_loan_agreement.pdf")
        pdf.output(path)
        return path

    def generate_esg_report(self):
        """Generate a realistic ESG sustainability report with metrics."""
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Page 1 - Cover
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 24)
        pdf.ln(30)
        pdf.cell(0, 15, "TechCorp Industries Ltd.", ln=True, align="C")
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 12, "Annual Sustainability Report", ln=True, align="C")
        pdf.cell(0, 12, "Financial Year 2026 (FY2026)", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 8, "Prepared in accordance with GRI Standards 2021", ln=True, align="C")
        pdf.cell(0, 8, "SASB Technology & Communications Sector", ln=True, align="C")
        pdf.ln(20)
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 8, "Report Period: April 1, 2025 - March 31, 2026", ln=True, align="C")
        pdf.cell(0, 8, "Published: June 15, 2026", ln=True, align="C")

        # Page 2 - Executive Summary
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, "1. EXECUTIVE SUMMARY", ln=True)
        pdf.ln(3)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "TechCorp Industries is pleased to present our FY2026 Sustainability Report, "
            "demonstrating our continued commitment to environmental stewardship and "
            "sustainable business practices. This report covers our environmental performance "
            "across key metrics including greenhouse gas emissions, energy consumption, "
            "water management, and waste reduction.\n\n"
            "Key Highlights for FY2026:\n"
            "- Scope 2 emissions reduced to 37,800 tCO2e (16% reduction from FY2023 baseline)\n"
            "- Renewable energy share increased to 28% of total consumption\n"
            "- Energy intensity improved to 74.5 MWh per million USD revenue\n"
            "- Water withdrawal reduced to 425,000 cubic meters\n"
            "- Waste diversion rate achieved at 78%\n\n"
            "We acknowledge that while significant progress has been made in most areas, "
            "our renewable energy adoption has fallen slightly short of our 30% target. "
            "We have initiated additional solar PPA contracts expected to close in Q1 FY2027."
        ))

        # Page 3 - GHG Emissions
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, "2. GREENHOUSE GAS EMISSIONS", ln=True)
        pdf.ln(3)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "GRI 305: Emissions\n\n"
            "TechCorp reports GHG emissions in accordance with the GHG Protocol Corporate "
            "Accounting and Reporting Standard. Emissions are reported using the market-based "
            "method for Scope 2, as required by our green loan covenants.\n"
        ))
        pdf.ln(3)

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "2.1 Scope 1 Emissions (Direct)", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "Scope 1 emissions include direct emissions from company-owned facilities, "
            "fleet vehicles, and on-site fuel combustion.\n\n"
            "FY2023 (Baseline): 12,500 tCO2e\n"
            "FY2024: 12,100 tCO2e\n"
            "FY2025: 11,800 tCO2e\n"
            "FY2026: 11,200 tCO2e\n\n"
            "Reduction from baseline: 10.4%\n"
            "Key driver: Fleet electrification program (35% of fleet now electric)"
        ))
        pdf.ln(5)

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "2.2 Scope 2 Emissions (Indirect - Energy)", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "Scope 2 emissions are calculated using the market-based method, accounting "
            "for renewable energy certificates (RECs) and power purchase agreements (PPAs).\n\n"
            "FY2023 (Baseline): 45,000 tCO2e\n"
            "FY2024: 43,200 tCO2e\n"
            "FY2025: 40,500 tCO2e\n"
            "FY2026: 37,800 tCO2e\n\n"
            "Reduction from baseline: 16.0%\n"
            "The 16% reduction exceeds our loan covenant target of 15% by FY2026. "
            "This was achieved through a combination of renewable energy procurement "
            "(solar PPA with SunPower Corp.), energy efficiency improvements across "
            "3 major manufacturing facilities, and operational optimization."
        ))
        pdf.ln(5)

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "2.3 Scope 3 Emissions (Value Chain)", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "Scope 3 emissions cover categories 1-7 of the GHG Protocol.\n\n"
            "FY2023: 125,000 tCO2e\n"
            "FY2024: 122,000 tCO2e\n"
            "FY2025: 118,000 tCO2e\n"
            "FY2026: 115,000 tCO2e\n\n"
            "Reduction from baseline: 8.0%"
        ))

        # Page 4 - Energy
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, "3. ENERGY MANAGEMENT", ln=True)
        pdf.ln(3)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, "GRI 302: Energy\n")
        pdf.ln(3)

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "3.1 Total Energy Consumption", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "FY2023 (Baseline): 850,000 MWh\n"
            "FY2024: 835,000 MWh\n"
            "FY2025: 810,000 MWh\n"
            "FY2026: 795,000 MWh\n\n"
            "Total reduction: 6.5% from baseline"
        ))
        pdf.ln(5)

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "3.2 Renewable Energy Share", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "Renewable energy as a percentage of total energy consumption:\n\n"
            "FY2023 (Baseline): 18%\n"
            "FY2024: 21%\n"
            "FY2025: 25%\n"
            "FY2026: 28%\n\n"
            "While we have made significant progress from our 18% baseline, "
            "we acknowledge that the FY2026 result of 28% falls short of our "
            "30% covenant target. The shortfall is primarily due to delays in "
            "commissioning our 50MW solar installation in Gujarat, which is now "
            "expected to be operational by Q2 FY2027. Upon full commissioning, "
            "our renewable energy share is projected to reach 34%.\n\n"
            "Renewable Energy Sources Breakdown (FY2026):\n"
            "- Solar PPA: 15% of total consumption\n"
            "- Wind Power (RECs): 8% of total consumption\n"
            "- Biomass: 3% of total consumption\n"
            "- Hydroelectric: 2% of total consumption"
        ))
        pdf.ln(5)

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "3.3 Energy Intensity", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "Energy intensity measured as MWh per million USD revenue:\n\n"
            "FY2023 (Baseline): 85.0 MWh/M USD\n"
            "FY2024: 81.2 MWh/M USD\n"
            "FY2025: 77.8 MWh/M USD\n"
            "FY2026: 74.5 MWh/M USD\n\n"
            "Improvement from baseline: 12.4%\n"
            "This exceeds our covenant target of 10% improvement (76.5 MWh/M USD). "
            "Key initiatives driving this improvement include LED lighting retrofits, "
            "HVAC optimization, smart building management systems, and process "
            "electrification in manufacturing."
        ))

        # Page 5 - Water
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, "4. WATER MANAGEMENT", ln=True)
        pdf.ln(3)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, "GRI 303: Water and Effluents\n")
        pdf.ln(3)

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "4.1 Total Water Withdrawal", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "FY2023 (Baseline): 500,000 m3\n"
            "FY2024: 480,000 m3\n"
            "FY2025: 455,000 m3\n"
            "FY2026: 425,000 m3\n\n"
            "Reduction from baseline: 15.0%\n\n"
            "While we have achieved a 15% reduction, this falls short of our 20% "
            "covenant target (400,000 m3). The gap of 25,000 m3 is attributed to "
            "increased production volumes in our semiconductor division. We have "
            "invested USD 5 million in a closed-loop water recycling system at our "
            "Bangalore facility, expected to deliver an additional 50,000 m3 annual "
            "savings starting FY2027."
        ))
        pdf.ln(5)

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "4.2 Water Recycling", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "Water recycled and reused:\n"
            "FY2023: 75,000 m3 (15% of withdrawal)\n"
            "FY2024: 95,000 m3 (19.8% of withdrawal)\n"
            "FY2025: 110,000 m3 (24.2% of withdrawal)\n"
            "FY2026: 130,000 m3 (30.6% of withdrawal)"
        ))

        # Page 6 - Waste
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, "5. WASTE MANAGEMENT", ln=True)
        pdf.ln(3)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, "GRI 306: Waste\n")
        pdf.ln(3)

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "5.1 Total Waste Generated", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "FY2023: 25,000 tonnes\n"
            "FY2024: 24,200 tonnes\n"
            "FY2025: 23,500 tonnes\n"
            "FY2026: 22,800 tonnes"
        ))
        pdf.ln(5)

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "5.2 Waste Diversion Rate", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "Waste diverted from landfill as a percentage of total waste:\n\n"
            "FY2023 (Baseline): 60%\n"
            "FY2024: 65%\n"
            "FY2025: 72%\n"
            "FY2026: 78%\n\n"
            "The FY2026 waste diversion rate of 78% exceeds our covenant target of 75%. "
            "This was achieved through expanded recycling programs, partnerships with "
            "certified waste management vendors, and implementation of a zero-waste-to-landfill "
            "policy at 2 of our 5 major facilities.\n\n"
            "Diversion Breakdown (FY2026):\n"
            "- Recycling: 52% (11,856 tonnes)\n"
            "- Composting: 12% (2,736 tonnes)\n"
            "- Waste-to-Energy: 14% (3,192 tonnes)\n"
            "- Landfill: 22% (5,016 tonnes)"
        ))

        # Page 7 - Summary Table
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, "6. ESG PERFORMANCE SUMMARY TABLE", ln=True)
        pdf.ln(5)

        pdf.set_font("Helvetica", "B", 10)
        col_w = [55, 30, 30, 30, 40]
        headers = ["KPI", "FY2023", "FY2025", "FY2026", "Target"]
        for i, h in enumerate(headers):
            pdf.cell(col_w[i], 8, h, border=1, align="C")
        pdf.ln()

        pdf.set_font("Helvetica", "", 9)
        data = [
            ["Scope 1 (tCO2e)", "12,500", "11,800", "11,200", "N/A"],
            ["Scope 2 (tCO2e)", "45,000", "40,500", "37,800", "38,250"],
            ["Scope 3 (tCO2e)", "125,000", "118,000", "115,000", "N/A"],
            ["Renewable Energy %", "18%", "25%", "28%", "30%"],
            ["Energy Intensity", "85.0", "77.8", "74.5", "76.5"],
            ["Water (000 m3)", "500", "455", "425", "400"],
            ["Waste Diversion %", "60%", "72%", "78%", "75%"],
        ]
        for row in data:
            for i, cell in enumerate(row):
                pdf.cell(col_w[i], 7, cell, border=1, align="C")
            pdf.ln()

        pdf.ln(10)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "7. ASSURANCE STATEMENT", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "This report has been subject to limited assurance by Ernst & Young LLP "
            "in accordance with ISAE 3000 (Revised). The assurance engagement covered "
            "Scope 1, Scope 2 emissions, energy consumption, and water withdrawal data.\n\n"
            "Signed: Dr. Priya Sharma, Chief Sustainability Officer\n"
            "Date: June 15, 2026"
        ))

        path = os.path.join(self.output_dir, "sample_esg_report.pdf")
        pdf.output(path)
        return path


if __name__ == "__main__":
    gen = SamplePDFGenerator()
    loan_path = gen.generate_loan_agreement()
    report_path = gen.generate_esg_report()
    print(f"Generated: {loan_path}")
    print(f"Generated: {report_path}")

from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date
from typing import Union, Literal, Optional, List

class Default(BaseModel):
    data:str
    
class PersonalDetails(BaseModel):
    name:str
    gender:str
    father_name: str
    mother_name:str
    dob:str
    address:str

class EmploymentDetails(BaseModel):
    occupation:str
    employer:str
    annual_income:str

class RealEstate(BaseModel):
    address:str
    value:Decimal
    is_pre_marital:bool

class Bank(BaseModel):
    bank_name:str
    account_number:str
    balance:Decimal

class Investment(BaseModel):
    type:str
    company:str
    value:Decimal
    is_pre_marital: bool

class Loan(BaseModel):
    type:str
    amount:Decimal
    bank:str

class Asset(BaseModel):
    real_estate:Optional[List[RealEstate]] = None
    bank_account:list[Bank]
    investment:Optional[List[Investment]] = None

class Liabilities(BaseModel):
    loans: Optional[List[Loan]] = None

class TotalInfo(BaseModel):
    personal:PersonalDetails
    employment:EmploymentDetails
    assets:Asset
    liabilities:Liabilities

class Submit(BaseModel):
    partyOne:TotalInfo
    partyTwo:TotalInfo
    execution_date:date
    marriage_date:date
    place_of_execution:str

    # --- SCHEMAS FOR WILL ---
class ExecutorDetails(BaseModel):
    name: str
    relationship: str
    address: str

class BeneficiaryDetails(BaseModel):
    name: str
    relationship: str
    address: str

class AssetBequest(BaseModel):
    asset_description: str
    beneficiary_name: str

class GuardianDetails(BaseModel):
    name: str
    relationship: str
    address: str

class WillSubmit(BaseModel):
    testator_name: str
    testator_father_name: str
    testator_age: str
    testator_address: str
    executors: list[ExecutorDetails]
    beneficiaries: list[BeneficiaryDetails]
    bequests: list[AssetBequest]
    residuary_beneficiary_name: str
    guardian: GuardianDetails | None = None
    execution_date: str
    place_of_execution: str    

   # --- SCHEMAS FOR COMMERCIAL RENTAL AGREEMENT ---
class LandlordDetails(BaseModel):
    name: str
    parent_name: str
    address: str

class IndividualTenantDetails(BaseModel):
    tenant_type: Literal["individual"]
    name: str
    parent_name: str
    address: str

class OrganizationTenantDetails(BaseModel):
    tenant_type: Literal["organization"]
    organization_name: str
    authorized_signatory: str
    registration_number: str | None = None
    address: str

class PremisesBoundaries(BaseModel):
    north: str
    south: str
    east: str
    west: str

class CRASubmit(BaseModel):
    execution_date: str 
    place_of_execution: str
    landlord: LandlordDetails
    tenant: Union[IndividualTenantDetails, OrganizationTenantDetails] = Field(..., discriminator='tenant_type')
    premises_address: str
    premises_boundaries: PremisesBoundaries
    start_date: str
    end_date: str
    rent_amount: str
    rent_amount_in_words: Optional[str] = None 
    rent_due_day: int
    security_deposit_amount: str
    security_deposit_in_words: Optional[str] = None
    security_deposit_refund_period_days: int
    permitted_business_use: str
    lock_in_period_months: int
    notice_period_months: int

    # --- SCHEMAS FOR SALE DEED ---
class VendorDetails(BaseModel):
    name: str
    parent_name: str
    address: str

class VendeeDetails(BaseModel):
    name: str
    parent_name: str
    address: str

class PropertyBoundaries(BaseModel):
    north: str
    south: str
    east: str
    west: str

class PaymentDetail(BaseModel):
    amount: str
    mode: str
    details: str

class SDSubmit(BaseModel):
    execution_date: str
    place_of_execution: str
    vendor: VendorDetails
    vendee: VendeeDetails
    property_address: str
    property_boundaries: PropertyBoundaries
    total_consideration: str
    total_consideration_in_words: Optional[str] = None
    payment_details: list[PaymentDetail]
    vendor_acquisition_method: str

class ResiRent(BaseModel):
    place_of_execution:str
    execution_date:str
    owner_name:str
    owner_father:str
    owner_address:str
    tenant_name:str
    tenant_father:str
    tenant_address:str
    premises_address:str
    rent_amount:str
    start_date:str
    end_date:str
    security_deposit_amount:str
    security_amount_words:str
    first_witness:str
    second_witness:str

# --- NEW SCHEMAS (FIXED) ---

# 1. NDA (Unchanged)
class NDASubmit(BaseModel):
    execution_date: str
    place_of_execution: str
    disclosing_party_name: str
    disclosing_party_address: str
    receiving_party_name: str
    receiving_party_address: str
    purpose_of_disclosure: str
    confidentiality_duration_years: str
    jurisdiction_city: str

# 2. Employment Contract (FIXED)
class EmploymentSubmit(BaseModel):
    execution_date: str
    place_of_execution: str
    employer_name: str
    employer_address: str
    employee_name: str
    employee_address: str
    designation: str
    start_date: str
    probation_period_months: str
    salary_amount: str
    # Changed from str to Optional[str] = None
    salary_amount_in_words: Optional[str] = None
    notice_period_days: str

# 3. Partnership (Unchanged)
class PartnerDetail(BaseModel):
    name: str
    address: str
    capital_contribution: str
    profit_share_percentage: str

class PartnershipSubmit(BaseModel):
    execution_date: str
    place_of_execution: str
    firm_name: str
    firm_address: str
    business_activity: str
    start_date: str
    partners: List[PartnerDetail]

# 4. Freelancer Agreement (FIXED)
class FreelancerSubmit(BaseModel):
    execution_date: str
    place_of_execution: str
    client_name: str
    client_address: str
    freelancer_name: str
    freelancer_address: str
    scope_of_work: str
    total_fee: str
    # Changed from str to Optional[str] = None
    total_fee_in_words: Optional[str] = None
    deadline_date: str

# 5. Service Agreement (Unchanged)
class ServiceSubmit(BaseModel):
    execution_date: str
    place_of_execution: str
    client_name: str
    client_address: str
    service_provider_name: str
    service_provider_address: str
    services_description: str
    payment_terms: str
    termination_notice_days: str

# 6. PoA (Unchanged)
class PoASubmit(BaseModel):
    execution_date: str
    place_of_execution: str
    principal_name: str
    principal_age: str
    principal_father_name: str
    principal_address: str
    attorney_name: str
    attorney_age: str
    attorney_father_name: str
    attorney_address: str
    purpose_of_poa: str
    specific_powers: List[str]

# 7. Affidavit (Unchanged)
class GeneralAffidavitSubmit(BaseModel):
    place_of_execution: str
    deponent_name: str
    deponent_father_name: str
    deponent_age: str
    deponent_address: str
    statement_paragraphs: List[str]
    verification_date: str

# 8. Name Change (Unchanged)
class NameChangeSubmit(BaseModel):
    place_of_execution: str
    deponent_old_name: str
    deponent_new_name: str
    deponent_father_name: str
    deponent_age: str
    deponent_address: str
    reason_for_change: str
    verification_date: str

# 9. Cease Desist (Unchanged)
class CeaseDesistSubmit(BaseModel):
    date_of_notice: str
    sender_name: str
    sender_address: str
    recipient_name: str
    recipient_address: str
    infringing_activity: str
    legal_rights_violated: str
    demand_action: str
    deadline_days: str

# 10. Legal Notice (FIXED)
class LegalNoticeSubmit(BaseModel):
    date_of_notice: str
    sender_name: str
    sender_address: str
    recipient_name: str
    recipient_address: str
    transaction_details: str
    outstanding_amount: str
    # Changed from str to Optional[str] = None
    outstanding_amount_in_words: Optional[str] = None
    payment_deadline_days: str
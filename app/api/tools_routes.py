from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel 

# Import all schemas
from app.schemas.schema import (
    Default, Submit, WillSubmit, CRASubmit, SDSubmit, ResiRent,
    NDASubmit, EmploymentSubmit, PartnershipSubmit, FreelancerSubmit,
    ServiceSubmit, PoASubmit, GeneralAffidavitSubmit, NameChangeSubmit,
    CeaseDesistSubmit, LegalNoticeSubmit
)

from app.services.utils import generate_docx_stream

# Import or define result_draft
from app.services.docs.mfa import result_draft

router = APIRouter(prefix="/docs")
templates = Jinja2Templates(directory="templates")

# Helper function to handle preview/download logic generically
def handle_doc_request(template_name: str, data: BaseModel, is_download: bool = False, filename: str = "document.docx"):
    try:
        template = templates.get_template(template_name)
        data_dict = data.model_dump()
        
        # Helper to fill "words" fields if missing
        for key in data_dict.keys():
            if key.endswith('_in_words') and not data_dict[key]:
                data_dict[key] = "______________________"

        rendered_text = template.render(**data_dict)
        
        if is_download:
            file_stream = generate_docx_stream(rendered_text)
            return StreamingResponse(
                file_stream,
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
        else:
            return {"data": rendered_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating {filename}: {str(e)}")

# --- MARITAL FINANCIAL ARRANGEMENT (MFA) ---

@router.post('/mfa_generator', response_model=Default)
def mfa_preview(data: Submit):
    """Phase 1: Generates text for preview only."""
    try:
        agreement = templates.get_template('mfa.html')
        rendered_text = agreement.render(**data.model_dump())
        print(rendered_text)
        return {"data": rendered_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating mfa preview: {str(e)}")

@router.post('/mfa_download')
def mfa_download(data: Submit):
    """Phase 2: Generates DOCX file and streams it for download."""
    try:
        agreement = templates.get_template('mfa.html')
        rendered_text = agreement.render(**data.model_dump())
        file_stream = generate_docx_stream(rendered_text)
        
        return StreamingResponse(
            file_stream,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=Last_Will_and_Testament.docx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating mfa file: {str(e)}")




# --- WILL GENERATOR ---
@router.post('/will_generator', response_model=Default)
def will_preview(data: WillSubmit):
    """Phase 1: Generates text for preview only."""
    try:
        agreement = templates.get_template('will.html')
        rendered_text = agreement.render(**data.model_dump())
        return {"data": rendered_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Will preview: {str(e)}")

@router.post('/will_download')
def will_download(data: WillSubmit):
    """Phase 2: Generates DOCX file and streams it for download."""
    try:
        agreement = templates.get_template('will.html')
        rendered_text = agreement.render(**data.model_dump())
        file_stream = generate_docx_stream(rendered_text)
        
        return StreamingResponse(
            file_stream,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=Last_Will_and_Testament.docx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Will file: {str(e)}")

# --- COMMERCIAL RENTAL AGREEMENT (CRA) ---

@router.post('/cra_generator', response_model=Default)
def cra_preview(data: CRASubmit):
    """Phase 1: Generates text for preview only using HTML template."""
    try:
        # Load the HTML template (which is now plain text)
        agreement = templates.get_template('cra.html')
        
        data_dict = data.model_dump()

        # Handle missing "words" fields cleanly so the template doesn't look broken
        if not data_dict.get('rent_amount_in_words'):
             data_dict['rent_amount_in_words'] = "______________________"
        if not data_dict.get('security_deposit_in_words'):
             data_dict['security_deposit_in_words'] = "______________________"

        # Render the template with the Pydantic model data
        rendered_text = agreement.render(
            **data_dict
        )
        return {"data": rendered_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating CRA preview: {str(e)}")

@router.post('/cra_download')
def cra_download(data: CRASubmit):
    """Phase 2: Generates DOCX file and streams it for download using HTML template."""
    try:
        agreement = templates.get_template('cra.html')
        
        data_dict = data.model_dump()
        if not data_dict.get('rent_amount_in_words'):
             data_dict['rent_amount_in_words'] = "______________________"
        if not data_dict.get('security_deposit_in_words'):
             data_dict['security_deposit_in_words'] = "______________________"
             
        rendered_text = agreement.render(
            **data_dict
        )
        file_stream = generate_docx_stream(rendered_text)
        
        return StreamingResponse(
            file_stream,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=Commercial_Rental_Agreement.docx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating CRA file: {str(e)}")


# --- SALE DEED (SD) ---

@router.post("/sd_generator", response_model=Default)
def sd_preview(data: SDSubmit):
    """Phase 1: Generates text for preview only."""
    try:
        agreement = templates.get_template('sd.html')
        data_dict = data.model_dump()
        
        # Handle missing "words" fields
        if not data_dict.get('total_consideration_in_words'):
             data_dict['total_consideration_in_words'] = "______________________"

        document_text = agreement.render(**data_dict)
        return {"data": document_text}  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Sale Deed preview: {str(e)}")

@router.post("/sd_download")
def sd_download(data: SDSubmit):
    """Phase 2: Generates DOCX file and streams it for download."""
    try:
        agreement = templates.get_template('sd.html')
        data_dict = data.model_dump()
        
        if not data_dict.get('total_consideration_in_words'):
             data_dict['total_consideration_in_words'] = "______________________"

        document_text = agreement.render(**data_dict)
        file_stream = generate_docx_stream(document_text)
        
        return StreamingResponse(
            file_stream,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=Sale_Deed.docx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Sale Deed file: {str(e)}")


# --- Residential Rental ---

@router.post("/rental_generator", response_model=Default)
def rental_preview(info: ResiRent):
    """Phase 1: Generates text for preview only."""
    try:
        agreement=templates.get_template('rental.html')
        rendered_text = agreement.render(   
        **info.model_dump()     
        )
        return {"data": rendered_text}  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Rental preview: {str(e)}")

@router.post('/rental_download')
def rental_download(info:ResiRent):
    
    try:
        agreement=templates.get_template('rental.html')
        rendered_text = agreement.render(   
        **info.model_dump()     
        ) 
        file_stream=generate_docx_stream(rendered_text)
        return StreamingResponse(
                file_stream,
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={"Content-Disposition": "attachment; filename=resi_rental.docx"}
            )
    except Exception as e:
        return HTTPException(
            status_code=500, 
            detail=f"Error generating Rental file: {str(e)}"
        )
    
# --- 1. NDA ---
@router.post('/nda_generator', response_model=Default)
def nda_preview(data: NDASubmit):
    return handle_doc_request('nda.html', data)

@router.post('/nda_download')
def nda_download(data: NDASubmit):
    return handle_doc_request('nda.html', data, True, "NDA.docx")

# --- 2. Employment Contract ---
@router.post('/employment_generator', response_model=Default)
def emp_preview(data: EmploymentSubmit):
    return handle_doc_request('employment.html', data)

@router.post('/employment_download')
def emp_download(data: EmploymentSubmit):
    return handle_doc_request('employment.html', data, True, "Employment_Contract.docx")

# --- 3. Partnership Agreement ---
@router.post('/partnership_generator', response_model=Default)
def partner_preview(data: PartnershipSubmit):
    return handle_doc_request('partnership.html', data)

@router.post('/partnership_download')
def partner_download(data: PartnershipSubmit):
    return handle_doc_request('partnership.html', data, True, "Partnership_Agreement.docx")

# --- 4. Freelancer Agreement ---
@router.post('/freelancer_generator', response_model=Default)
def free_preview(data: FreelancerSubmit):
    return handle_doc_request('freelancer.html', data)

@router.post('/freelancer_download')
def free_download(data: FreelancerSubmit):
    return handle_doc_request('freelancer.html', data, True, "Freelancer_Agreement.docx")

# --- 5. Service Agreement ---
@router.post('/service_generator', response_model=Default)
def service_preview(data: ServiceSubmit):
    return handle_doc_request('service.html', data)

@router.post('/service_download')
def service_download(data: ServiceSubmit):
    return handle_doc_request('service.html', data, True, "Service_Agreement.docx")

# --- 6. Power of Attorney ---
@router.post('/poa_generator', response_model=Default)
def poa_preview(data: PoASubmit):
    return handle_doc_request('poa.html', data)

@router.post('/poa_download')
def poa_download(data: PoASubmit):
    return handle_doc_request('poa.html', data, True, "Power_of_Attorney.docx")

# --- 7. General Affidavit ---
@router.post('/affidavit_generator', response_model=Default)
def affidavit_preview(data: GeneralAffidavitSubmit):
    return handle_doc_request('affidavit.html', data)

@router.post('/affidavit_download')
def affidavit_download(data: GeneralAffidavitSubmit):
    return handle_doc_request('affidavit.html', data, True, "General_Affidavit.docx")

# --- 8. Name Change Affidavit ---
@router.post('/namechange_generator', response_model=Default)
def namechange_preview(data: NameChangeSubmit):
    return handle_doc_request('name_change.html', data)

@router.post('/namechange_download')
def namechange_download(data: NameChangeSubmit):
    return handle_doc_request('name_change.html', data, True, "Name_Change_Affidavit.docx")

# --- 9. Cease & Desist Letter ---
@router.post('/ceasedesist_generator', response_model=Default)
def cd_preview(data: CeaseDesistSubmit):
    return handle_doc_request('cease_desist.html', data)

@router.post('/ceasedesist_download')
def cd_download(data: CeaseDesistSubmit):
    return handle_doc_request('cease_desist.html', data, True, "Cease_Desist_Letter.docx")

# --- 10. Legal Notice ---
@router.post('/legalnotice_generator', response_model=Default)
def notice_preview(data: LegalNoticeSubmit):
    return handle_doc_request('legal_notice.html', data)

@router.post('/legalnotice_download')
def notice_download(data: LegalNoticeSubmit):
    return handle_doc_request('legal_notice.html', data, True, "Legal_Notice.docx")    
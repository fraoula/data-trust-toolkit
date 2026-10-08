import json, sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

SENSITIVE_FIELDS={
    'ssn','social_security_number','email','email_address','phone','phone_number',
    'mobile','mobile_number','dob','date_of_birth','passport','passport_number',
    'credit_card','card_number','cvv','bank_account','iban','aadhaar','aadhar','pan',
    'tax_id','medical_record_number','mrn'
}

class SchemaError(ValueError): pass

def load_schema(path: str|Path)->Dict[str,str]:
    p=Path(path)
    if not p.exists(): raise SchemaError(f'Schema file not found: {p}')
    try: data=json.loads(p.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e: raise SchemaError(f'Invalid JSON in {p}: line {e.lineno}, column {e.colno}') from e
    if not isinstance(data,dict): raise SchemaError(f'Schema must be a JSON object: {p}')
    out={}
    for field,typ in data.items():
        if not isinstance(field,str) or not field.strip(): raise SchemaError('Every field name must be a non-empty string.')
        if not isinstance(typ,str) or not typ.strip(): raise SchemaError(f"Type for field '{field}' must be a non-empty string.")
        out[field.strip()]=typ.strip().lower()
    return out

def normalize_name(name:str)->str:
    return name.strip().lower().replace('-','_').replace(' ','_')

def is_sensitive_field(field:str, sensitive_fields:Iterable[str]=SENSITIVE_FIELDS)->bool:
    n=normalize_name(field)
    return n in {normalize_name(x) for x in sensitive_fields}

def compare_schemas(baseline:Dict[str,str], incoming:Dict[str,str])->Tuple[List[str],List[str],List[str]]:
    breaking=[]; warnings=[]; safe=[]
    for field in sorted(baseline):
        if field not in incoming: breaking.append(f'Required field removed: {field}')
    for field in sorted(baseline):
        if field in incoming and baseline[field]!=incoming[field]:
            breaking.append(f'{field}: {baseline[field]} → {incoming[field]}')
    for field in sorted(incoming):
        if field not in baseline:
            (warnings if is_sensitive_field(field) else safe).append(
                f"New sensitive field detected: {field}" if is_sensitive_field(field) else f"Optional field added: {field}"
            )
    return breaking,warnings,safe

def calculate_risk(breaking:List[str], warnings:List[str])->int:
    return min(len(breaking)*30 + len(warnings)*10, 100)

def determine_status(breaking:List[str], warnings:List[str])->str:
    return 'FAIL' if breaking else ('WARN' if warnings else 'PASS')

def render_report(breaking:List[str],warnings:List[str],safe:List[str])->str:
    lines=['','Fraoula Schema Drift Report','='*30,'',f'Status: {determine_status(breaking,warnings)}',f'Risk Score: {calculate_risk(breaking,warnings)}/100']
    if breaking: lines += ['','BREAKING'] + [f'✗ {x}' for x in breaking]
    if warnings: lines += ['','WARNING'] + [f'⚠ {x}' for x in warnings]
    if safe: lines += ['','SAFE'] + [f'✓ {x}' for x in safe]
    if not breaking and not warnings and not safe: lines += ['','No schema drift detected.']
    lines += ['','Powered by Fraoula','https://www.fraoula.co','']
    return '\n'.join(lines)

def main(argv=None)->int:
    args=list(argv if argv is not None else sys.argv[1:])
    if len(args)!=2:
        print('Usage: python drift_guard.py <baseline.json> <incoming.json>',file=sys.stderr); return 2
    try: baseline=load_schema(args[0]); incoming=load_schema(args[1])
    except SchemaError as e: print(f'Schema Drift Guard error: {e}',file=sys.stderr); return 2
    breaking,warnings,safe=compare_schemas(baseline,incoming)
    print(render_report(breaking,warnings,safe))
    return 1 if breaking else 0

if __name__=='__main__': raise SystemExit(main())

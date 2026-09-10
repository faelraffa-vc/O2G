# -*- coding: utf-8 -*-
"""Gera assets/Old-to-Gold-Guide.pdf, o guia entregue pelo botao da home.

Como rodar:
    python3 -m venv .venv && .venv/bin/pip install reportlab
    .venv/bin/python tools/build-guide.py
    mv Old-to-Gold-Guide.pdf assets/


Conteudo vindo de Website.docx (secoes "How We Choose a Property",
"Different Ways to Buy a Property in Ireland" e "Government Grant Application").
Fontes da marca nao existem nesta maquina, entao sai em Helvetica."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, KeepTogether, Table, TableStyle, PageBreak, Image, CondPageBreak,
                                NextPageTemplate)

PAPER=HexColor("#FBF9F6"); INK=HexColor("#17130F"); MID=HexColor("#5E554B")
PINK=HexColor("#CE3369"); GOLD=HexColor("#F0C040"); GOLDD=HexColor("#8A6A12")
SAND=HexColor("#F4EDE3"); LINE=HexColor("#E0D6C8"); NIGHT=HexColor("#141110")
W,H=A4; M=20*mm

S=lambda **k: ParagraphStyle(**k)
h1=S(name='h1',fontName='Helvetica-Bold',fontSize=21,leading=25,textColor=INK,spaceBefore=6,spaceAfter=7)
h2=S(name='h2',fontName='Helvetica-Bold',fontSize=13.5,leading=17,textColor=INK,spaceBefore=13,spaceAfter=5)
h3=S(name='h3',fontName='Helvetica-Bold',fontSize=10.5,leading=14,textColor=PINK,spaceBefore=10,spaceAfter=3)
body=S(name='body',fontName='Helvetica',fontSize=9.8,leading=14.6,textColor=MID,spaceAfter=6,alignment=TA_LEFT)
lead=S(name='lead',fontName='Helvetica',fontSize=11.5,leading=17,textColor=MID,spaceAfter=8)
bullet=S(name='bul',fontName='Helvetica',fontSize=9.8,leading=14.4,textColor=MID,
         leftIndent=11,bulletIndent=1,spaceAfter=2.5)
quote=S(name='q',fontName='Helvetica-Bold',fontSize=11,leading=15.5,textColor=INK,
        leftIndent=10,spaceBefore=6,spaceAfter=8)
small=S(name='sm',fontName='Helvetica',fontSize=7.8,leading=11,textColor=HexColor("#7E7367"))

def bg(c,d):
    c.setFillColor(PAPER); c.rect(0,0,W,H,fill=1,stroke=0)

def chrome(c,d):
    bg(c,d)
    c.setFillColor(PINK); c.rect(0,H-9*mm,W,9*mm,fill=1,stroke=0)
    c.setFillColor(HexColor("#FFFFFF")); c.setFont("Helvetica-Bold",7.2)
    c.drawString(M,H-6*mm,"OLD TO GOLD")
    c.setFont("Helvetica",7.2)
    c.drawRightString(W-M,H-6*mm,"How to rebuild a derelict house")
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M,15*mm,W-M,15*mm)
    c.setFillColor(HexColor("#7E7367")); c.setFont("Helvetica",7.4)
    c.drawString(M,10.5*mm,"oldtogold.ie  ·  contact@oldtogold.ie  ·  Limerick, Ireland")
    c.drawRightString(W-M,10.5*mm,str(c.getPageNumber()))

def cover(c,d):
    bg(c,d)
    c.setFillColor(NIGHT); c.rect(0,H-118*mm,W,118*mm,fill=1,stroke=0)
    c.setFillColor(PINK); c.rect(M,H-46*mm,26*mm,1.6*mm,fill=1,stroke=0)
    c.setFillColor(HexColor("#FFFFFF")); c.setFont("Helvetica-Bold",8.5)
    c.drawString(M,H-22*mm,"OLD TO GOLD")
    c.setFont("Helvetica",8.5); c.setFillColor(HexColor("#FFFFFFAA"))
    c.drawString(M,H-29*mm,"Limerick, Ireland")
    c.setFillColor(HexColor("#FFFFFF")); c.setFont("Helvetica-Bold",34)
    c.drawString(M,H-64*mm,"How to rebuild")
    c.drawString(M,H-79*mm,"a ")
    c.setFillColor(GOLD); c.drawString(M+c.stringWidth("a ","Helvetica-Bold",34),H-79*mm,"derelict house.")
    c.setFillColor(HexColor("#FFFFFFB0")); c.setFont("Helvetica",11)
    c.drawString(M,H-95*mm,"Choosing the property, paying for it, and claiming the grant.")
    c.drawString(M,H-102*mm,"Written from doing it ourselves in Limerick.")
    # tres marcadores
    y=H-150*mm
    for n,t in [("01","Choosing a property to buy and rent"),
                ("02","Different ways to buy in Ireland"),
                ("03","The Vacant Property Refurbishment Grant")]:
        c.setFillColor(GOLDD); c.setFont("Helvetica-Bold",15); c.drawString(M,y,n)
        c.setFillColor(INK); c.setFont("Helvetica-Bold",11); c.drawString(M+14*mm,y,t)
        c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M,y-5*mm,W-M,y-5*mm)
        y-=15*mm
    c.setFillColor(HexColor("#7E7367")); c.setFont("Helvetica",8)
    c.drawString(M,22*mm,"This guide is general information, not financial, legal or tax advice.")
    c.drawString(M,17.5*mm,"Figures and rules change. Confirm current requirements with the relevant authority before you act.")

def P(t,s=body): return Paragraph(t,s)
def UL(items,st=bullet): return [Paragraph(i,st,bulletText='—') for i in items]

cellst=S(name='cell',fontName='Helvetica',fontSize=9,leading=12.4,textColor=MID)
cellhd=S(name='cellhd',fontName='Helvetica-Bold',fontSize=8.6,leading=11.4,textColor=INK)

def panel(rows,head=None,widths=None,shade=SAND):
    """Celula tem que ser Paragraph: string pura nao quebra linha e vaza a margem."""
    FW=W-2*M-1
    n=len(rows[0])
    if widths is None:
        widths=[FW/n]*n
    else:
        fixed=sum(w for w in widths if w); k=widths.count(None)
        widths=[(w if w else (FW-fixed)/k) for w in widths]
    data=[]
    if head: data.append([Paragraph(h,cellhd) for h in head])
    for r in rows: data.append([Paragraph(c,cellst) for c in r])
    t=Table(data,colWidths=widths,hAlign='LEFT')
    st=[('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-2),.5,LINE),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7)]
    if head: st+=[('BACKGROUND',(0,0),(-1,0),shade)]
    t.setStyle(TableStyle(st)); return t

F=[]
A=F.append

# ── 01 ─────────────────────────────────────────────────────────────
A(P("Choosing a property to buy and rent",h1))
A(P("Finding the right property is about more than finding a cheap house.",lead))
A(P("Buying a property to rent is not simply about finding the lowest purchase price. A property can look like a bargain on paper and become an expensive mistake if the location is wrong, the refurbishment costs are underestimated, the rental income does not support the investment, or there are planning, structural or legal issues that were not identified before purchase.",body))
A(P("We look at the whole investment picture before deciding whether a property is right. Our approach focuses on properties that have been vacant, neglected or need significant refurbishment, because those are where value can still be created through the right renovation and long-term management.",body))

A(P("Step 1. Start with the end goal",h2))
A(P("Before looking at individual properties, ask what you are trying to achieve. In our case the objective is to buy, refurbish, rent and hold as a long-term investment. That means you need to know what the finished property should look like before you decide what you are prepared to pay for it.",body))
A(P("What we work out first",h3))
for p in UL([
 "What type of tenant are we trying to attract?",
 "What type of property is in demand in the area?",
 "What rent could the finished property realistically achieve?",
 "How much refurbishment will be required?",
 "What will the property be worth once the work is completed?",
 "How much capital can we invest, and what financing is available?",
 "What will the ongoing costs be, and will the return be acceptable?"]): A(p)
A(P("The purchase price is only one part of the calculation.",quote))

A(P("Step 2. Choose the right location",h2))
A(P("For a rental investment, location is critical. A beautiful property in the wrong location can be much harder to rent than a modest property in an area with strong and consistent rental demand.",body))
A(panel([
 ["Employment","Major employers, business parks, hospitals or universities nearby."],
 ["Transport","How easily tenants reach public transport, roads and key destinations."],
 ["Education","Schools, colleges and universities within reach."],
 ["Amenities","Shops, supermarkets, healthcare, parks and everyday facilities."],
 ["Rental demand","Whether similar properties in the area are being let quickly."],
 ["Tenant profile","Who is likely to rent it. A young professional and a family want different things."],
 ["Future development","Planned developments or infrastructure that could affect the area either way."],
],head=["Factor","What we look at"],widths=[36*mm,None]))
A(Spacer(1,6))
A(P("We do not just ask whether we can buy the property cheaply. We ask whether people will want to live there.",quote))

A(P("Step 3. Establish the realistic rental income",h2))
A(P("Before buying, you need to understand what the property could realistically rent for after refurbishment. Compare similar properties in the local market and account for size, number of bedrooms and bathrooms, condition, BER rating, quality of the refurbishment, parking, garden or outdoor space, transport links and location.",body))
A(P("Ireland's rent rules affect the answer",h3))
A(P("Since 1 March 2026, national rent-control rules apply to private tenancies, with specific rules governing rent increases and when a new tenancy can be set at market rent. The RTB also requires landlords to use appropriate market evidence when setting rent in circumstances where market rent can be applied.",body))
A(P("This means an investment decision cannot rest on what you hope the property will rent for. The numbers have to work within the rules that actually apply to that property. Confirm the current position with the RTB before you commit.",body))

A(P("Step 4. Look beyond the purchase price",h2))
A(P("A property advertised at €180,000 is not necessarily a €180,000 investment. Before you decide what it really costs, add up everything that has to be paid before the first tenant moves in.",body))
A(panel([
 ["Purchase price","What you agree to pay, not the asking price."],
 ["Overbidding","Anything paid above affordability because of competition."],
 ["Stamp duty","Plus other acquisition costs."],
 ["Legal fees","Solicitor and conveyancing."],
 ["Survey","Surveyor or engineer reports."],
 ["Mortgage protection","Where required by the lender."],
 ["Planning","Where the works need it."],
 ["Refurbishment","The works themselves, with a contingency."],
],head=["Cost","Note"],widths=[42*mm,None]))
A(CondPageBreak(120*mm))

# ── 02 ─────────────────────────────────────────────────────────────
A(P("Different ways to buy a property in Ireland",h1))
A(P("There is more than one way to finance a purchase. For many people the most common route is a mortgage from a bank or other lender. Depending on your circumstances there are other possibilities: your own savings, investment partners, inheritance, selling another asset, or raising finance against a property you already own.",body))
A(P("The right option depends on your income, financial position, available capital, credit history, the type of property and what you intend to do with it. Before deciding, understand not only how much money you can access but what that money costs and how it affects the investment.",body))

A(P("1. A cash purchase",h2))
A(P("The simplest option is buying with money you already have. No mortgage application, no interest, no monthly repayments, a faster and potentially simpler transaction, a stronger position when negotiating, and more control over the property.",body))
A(P("Buying with cash still has costs",h3))
A(P("Stamp duty, solicitor and conveyancing costs, survey and professional fees, refurbishment, insurance, ongoing maintenance and any other applicable purchase costs all remain.",body))
A(P("If you use all your savings on the purchase, you may have very little left for refurbishment, emergencies or the unexpected. On an investment property, cash reserves matter as much as the purchase price.",quote))

A(P("2. A bank mortgage",h2))
A(P("Instead of paying the whole price yourself, you contribute part and borrow the rest. On a €300,000 property that might mean a €60,000 deposit from you and €240,000 from the lender, repaid over the agreed term with interest.",body))
A(P("What you can borrow depends on your income, financial commitments, credit history, the property and the lender's criteria. For an investment property the lending rules can be different from those for a home you intend to live in.",body))
A(panel([
 ["You do not need the full price available","Mortgage repayments"],
 ["Leverage lets you acquire a larger asset","Interest rates"],
 ["Your capital can spread across investments","Vacancies and lost rental income"],
 ["","Maintenance, insurance and the unexpected"],
 ["","Changes in the property market"],
],head=["Advantages","What you take on"],widths=[None,None]))
A(Spacer(1,6))
A(P("Borrowing creates an obligation. The investment has to stay viable even when things do not go to plan.",quote))

A(P("3. Raising finance against a property you own",h2))
A(P("If you already own a property that has risen in value, you may be able to approach a lender about borrowing against that equity, subject to their assessment and criteria. The funds could go towards another purchase or project.",body))
A(panel([
 ["Property value","€400,000"],
 ["Outstanding mortgage","€150,000"],
 ["Gross equity","€250,000"],
],head=["Worked example","Amount"],widths=[None,40*mm]))
A(Spacer(1,6))
A(P("Gross equity of €250,000 does not mean you can borrow €250,000. The lender will assess the property, your income, existing debt and affordability before deciding what, if anything, is available.",body))
A(CondPageBreak(120*mm))

# ── 03 ─────────────────────────────────────────────────────────────
A(P("The Vacant Property Refurbishment Grant",h1))
A(P("Croí Cónaithe Towns Fund. What you need, in the order the council asks for it.",lead))
A(P("This is the part most people find hardest, because the paperwork comes in two waves: once to get approved, and again after the work is finished to actually get paid. What follows is the sequence we went through.",body))

A(P("First wave. Getting approved",h2))
A(panel([
 ["Application form","The proposed works you intend to carry out, with the cost stated for each one."],
 ["Quotation","From the contractor or supplier."],
 ["Engineering report",""],
 ["Proof of ownership","Solicitor letter, plus the Revenue stamp certificate."],
 ["Proof of status","ESB letter showing the property is vacant, or a council letter showing it is derelict."],
],head=["Document","Detail"],widths=[42*mm,None]))
A(Spacer(1,7))
A(P("If the application is approved you receive an approval letter setting out the amount and the conditions attached to it.",body))

A(P("What the approval letter ties you to",h3))
A(P("Approval is granted from the date of issue and is valid for a limited period, so the works have to be planned around that window. The conditions typically include a final site inspection of the completed works by the local authority, proof of ownership before drawdown, compliance with all relevant planning and building regulations, a legal charge over the property as security for the grant, and the clawback provisions below.",body))
A(P("For a rental property specifically, the applicant must make the property available for rent and register the tenancy with the RTB before drawdown, and ensure the property complies with fire safety and minimum standards regulations.",body))

A(P("Clawback. The condition people miss",h2))
A(P("The grant is repayable if the property changes use or is sold inside the clawback period. The period runs from the date the funding is transferred, not from approval.",body))
A(panel([
 ["Within 5 years","100% of the grant is repayable"],
 ["Over 5 and up to 10 years","75% of the grant is repayable"],
 ["Over 10 years","No clawback applies"],
],head=["Property sold, or ceases to be a principal private residence or an RTB-registered rental","Clawback"],widths=[None,38*mm]))
A(Spacer(1,7))
A(P("A grant is not free money if you might sell in year three. Decide the holding period before you apply.",quote))

A(P("Second wave. Getting paid after the works",h2))
A(P("Once the refurbishment is finished, the council needs the full evidence trail before releasing funds.",body))
A(panel([
 ["1. Cost breakdown","Set out the completed works by category, with the cost of each."],
 ["2. Supplier and payment setup","The council's supplier and payment details form."],
 ["3. Invoice summary sheet","Every invoice numbered, with contractor, date and amount, and tax clearance attached for each one."],
 ["4. Proof of payment","Bank statements with the payments to contractors highlighted and identified, all receipts, and copies of any cheques issued."],
],head=["Step","What it contains"],widths=[42*mm,None]))
A(Spacer(1,7))

A(P("Which works count",h3))
A(P("The cost breakdown is organised by category. Demolition, strip out and site clearance including removal of hazardous waste. Substructure works including foundations, rising walls, floor slabs, damp-proofing and underpinning. Structural works to the superstructure including walls, party walls, chimneys, suspended timber floors and structural timbers. Internal walls, stairs and landings, including doors, windows and applied finishes. External wall completions including doors, windows, sills and applied finishes. Roof completions including flashings, fascia, soffits, gutters and downpipes. Building services: plumbing, heating, ventilation, electrical and telecommunications. Painting and decoration required because of the works carried out. An extension within the ambit of exempt development, as part of a wider refurbishment. Necessary external and site development works within the curtilage. Professional services associated with the works.",body))

A(P("Also required before payment",h3))
for p in UL([
 "Tax clearance certificate for every contractor supplying goods or services over €10,000.",
 "Confirmation from Revenue that Local Property Tax is paid up to date.",
 "Evidence of home insurance, with the policy updated to reflect the rental value if you applied as a rental.",
 "SEAI confirmation, by letter or email, that the grant-funded works received no funding from them, quoting the MPRN and the property address.",
]): A(p)
A(Spacer(1,4))
A(P("When all the documentation is approved you receive an appointment for the property inspection, and after that confirmation by email that payment is coming. Payments are made on Fridays.",body))

A(P("Plan for six months, or longer",h2))
A(P("The overall process may take six months or more. Do not make commitments or give anyone a specific repayment date based on the grant, because there is no guaranteed timeline for when the funds arrive. Build the delay into your cash flow from the start.",body))
A(Spacer(1,10))

A(KeepTogether([
 P("Where to go from here",h1),
 P("We are not consultants. We buy these houses ourselves, and everything in this guide is what we learned doing it. If you are working on a property in Limerick and something here does not match what you are being told, write to us and ask.",lead),
 Spacer(1,4),
 panel([
 ["Talk to us","contact@oldtogold.ie"],
 ["Our own projects","Three houses in Limerick, with the real figures published"],
 ["If you own a property","Ask about Rent-to-Rent and hand over the management"],
],head=["Next step","Where"],widths=[42*mm,None],shade=HexColor("#F7E3EC")),Spacer(1,9),
 P("This guide is general information based on our own experience in Limerick. It is not financial, legal, tax or planning advice, and it is not a recommendation to invest. Grant terms, tenancy rules and lending criteria change, and they vary by property and by local authority. Confirm the current requirements with the relevant authority, and take advice from a qualified professional, before you commit money. Old to Gold accepts no liability for decisions taken on the basis of this document.",small),
 P("Old to Gold, Limerick, Ireland. contact@oldtogold.ie",small)]))

# ── build ──────────────────────────────────────────────────────────
doc=BaseDocTemplate("Old-to-Gold-Guide.pdf",pagesize=A4,
    leftMargin=M,rightMargin=M,topMargin=18*mm,bottomMargin=20*mm,
    title="How to rebuild a derelict house",author="Old to Gold",
    subject="Choosing a property, paying for it, and claiming the Vacant Property Refurbishment Grant")
fr=Frame(M,20*mm,W-2*M,H-18*mm-20*mm,id='n')
doc.addPageTemplates([
    PageTemplate(id='cover',frames=[Frame(M,20*mm,W-2*M,H-40*mm,id='c')],onPage=cover),
    PageTemplate(id='body',frames=[fr],onPage=chrome),
])
# PageBreak sozinho nao troca de template: precisa do NextPageTemplate.
F.insert(0,PageBreak())
F.insert(0,NextPageTemplate('body'))
doc.build(F)
print("ok")

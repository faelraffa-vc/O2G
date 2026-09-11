# -*- coding: utf-8 -*-
"""Gera assets/Old-to-Gold-Guide.pdf, o guia entregue pelo botao do site.

Como rodar (a partir da raiz do repositorio):
    python3 -m venv .venv && .venv/bin/pip install reportlab
    .venv/bin/python tools/build-guide.py

Conteudo: Website.docx, secoes "How We Choose a Property", "Different Ways
to Buy a Property in Ireland" e "Government Grant Application".
Tipografia e paleta sao as mesmas do index.html: Bricolage Grotesque no
display, Instrument Sans no texto, off-white com rosa e dourado.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, KeepTogether, Table, TableStyle, PageBreak,
                                Image, NextPageTemplate, CondPageBreak, Flowable)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
F_DIR = os.path.join(HERE, 'fonts')
A_DIR = os.path.join(ROOT, 'assets', 'pdf')
OUT   = os.path.join(ROOT, 'assets', 'Old-to-Gold-Guide.pdf')

# ── Tipografia do site ────────────────────────────────────────────────
for name, file in [('Bri', 'Bricolage-Bold.ttf'), ('BriSB', 'Bricolage-SemiBold.ttf'),
                   ('Ins', 'Instrument-Regular.ttf'), ('InsSB', 'Instrument-SemiBold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(F_DIR, file)))

# ── Paleta do site ────────────────────────────────────────────────────
PAPER=HexColor("#FBF9F6"); CARD=HexColor("#FFFFFF"); SAND=HexColor("#F4EDE3")
SHELL=HexColor("#F1E9DD"); LINE=HexColor("#E7DED2")
INK=HexColor("#17130F"); MID=HexColor("#6E6459"); SOFT=HexColor("#7E7367")
PINK=HexColor("#E8457C"); PINKB=HexColor("#CE3369"); PINKD=HexColor("#B32C5E")
GOLD=HexColor("#F0C040"); GOLDD=HexColor("#8A6A12"); NIGHT=HexColor("#141110")

W,H=A4; M=19*mm; FW=W-2*M

def WA(a):
    """Branco com alfa. WA(.50) nao funciona aqui."""
    return Color(1,1,1,a)

S=lambda **k: ParagraphStyle(**k)
h1   =S(name='h1',fontName='Bri',fontSize=23,leading=26,textColor=INK,spaceAfter=8)
h2   =S(name='h2',fontName='Bri',fontSize=14,leading=18,textColor=INK,spaceBefore=15,spaceAfter=6)
h3   =S(name='h3',fontName='BriSB',fontSize=11,leading=14,textColor=PINKD,spaceBefore=11,spaceAfter=4)
body =S(name='body',fontName='Ins',fontSize=9.9,leading=15,textColor=MID,spaceAfter=7)
lead =S(name='lead',fontName='Ins',fontSize=12,leading=18,textColor=MID,spaceAfter=9)
bul  =S(name='bul',fontName='Ins',fontSize=9.9,leading=15,textColor=MID,leftIndent=12,bulletIndent=1,spaceAfter=3,
         bulletFontName='Ins',bulletFontSize=9.9,bulletColor=PINKB)
pull =S(name='pull',fontName='BriSB',fontSize=12.5,leading=17,textColor=INK)
small=S(name='sm',fontName='Ins',fontSize=8,leading=11.6,textColor=SOFT)
cardt=S(name='ct',fontName='BriSB',fontSize=10.4,leading=13,textColor=INK,spaceAfter=3)
cardb=S(name='cb',fontName='Ins',fontSize=9.2,leading=13,textColor=MID)
num  =S(name='nm',fontName='Bri',fontSize=27,leading=29,textColor=INK)
white=S(name='wh',fontName='Ins',fontSize=10,leading=14.5,textColor=WA(.70))

def P(t,s=body): return Paragraph(t,s)
def UL(items): return [Paragraph(i,bul,bulletText='—') for i in items]

# ── Cartao arredondado, o "bezel" do site ─────────────────────────────
def card(inner, bg=CARD, border=LINE, pad=11, radius=13, width=None):
    t=Table([[inner]], colWidths=[width or FW], hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('BOX',(0,0),(-1,-1),0.7,border),
        ('ROUNDEDCORNERS',[radius,radius,radius,radius]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),pad),('RIGHTPADDING',(0,0),(-1,-1),pad),
        ('TOPPADDING',(0,0),(-1,-1),pad),('BOTTOMPADDING',(0,0),(-1,-1),pad),
    ]))
    return t

def cards_row(items, gap=7, bg=CARD, border=LINE, pad=11, radius=13, rowh=None):
    """Fileira de cartoes com respiro entre eles, como o grid do site."""
    n=len(items)
    cw=(FW-2-gap*(n-1))/n
    cells=[]
    for it in items:
        cells.append(card(it,bg=bg,border=border,pad=pad,radius=radius,width=cw))
        cells.append('')
    cells=cells[:-1]
    widths=[]
    for i in range(n):
        widths.append(cw)
        if i<n-1: widths.append(gap)
    t=Table([cells],colWidths=widths,rowHeights=[rowh] if rowh else None,hAlign='LEFT')
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
        ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    return t

def rows(pairs, head=None, w1=44*mm, bg=CARD, shade=SAND):
    """Tabela dentro de um cartao, com a primeira coluna em destaque."""
    data=[]
    if head: data.append([Paragraph(head[0],cardt),Paragraph(head[1],cardt)])
    for a,b in pairs:
        data.append([Paragraph(a,S(name='k',fontName='InsSB',fontSize=9.2,leading=13,textColor=INK)),
                     Paragraph(b,cardb)])
    t=Table(data,colWidths=[w1,FW-w1-22],hAlign='LEFT')
    st=[('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LINEBELOW',(0,0),(-1,-2),0.6,LINE),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8)]
    if head: st.append(('LINEBELOW',(0,0),(-1,0),0.9,INK))
    t.setStyle(TableStyle(st))
    return card(t,bg=bg,pad=13)

class Rule(Flowable):
    def __init__(self,w=FW,col=LINE,h=0.7): self.w,self.col,self.h=w,col,h
    def wrap(self,*a): return (self.w,self.h+8)
    def draw(self):
        self.canv.setStrokeColor(self.col); self.canv.setLineWidth(self.h)
        self.canv.line(0,4,self.w,4)

def grad_word(c,x,y,text,font,size,c1,c2):
    """Escreve letra a letra interpolando a cor, para reproduzir o
    gradiente rosa->dourado que o site aplica na palavra 'gold'."""
    n=max(1,len(text)-1)
    for i,ch in enumerate(text):
        t=i/n
        c.setFillColor(Color(c1.red+(c2.red-c1.red)*t,
                             c1.green+(c2.green-c1.green)*t,
                             c1.blue+(c2.blue-c1.blue)*t))
        c.setFont(font,size); c.drawString(x,y,ch)
        x+=c.stringWidth(ch,font,size)
    return x

def wordmark(c,x,y,size,dim=SOFT,on_dark=False):
    c.setFont('Bri',size)
    c.setFillColor(HexColor("#FFFFFF") if on_dark else INK); c.drawString(x,y,"old ")
    x+=c.stringWidth("old ",'Bri',size)
    c.setFillColor(WA(.40) if on_dark else dim); c.drawString(x,y,"to ")
    x+=c.stringWidth("to ",'Bri',size)
    return grad_word(c,x,y,"gold",'Bri',size,PINK,GOLD)

# ── Arte de pagina ────────────────────────────────────────────────────
def bg(c):
    c.setFillColor(PAPER); c.rect(0,0,W,H,fill=1,stroke=0)

def cover(c,d):
    bg(c)
    # bloco escuro do topo, com a foto sangrando a direita
    c.saveState()
    p=c.beginPath(); p.rect(0,H-128*mm,W,128*mm); c.clipPath(p,stroke=0)
    c.setFillColor(NIGHT); c.rect(0,H-128*mm,W,128*mm,fill=1,stroke=0)
    try:
        c.drawImage(os.path.join(A_DIR,'nina-studio.jpg'),W-96*mm,H-128*mm,
                    width=96*mm,height=128*mm,mask='auto',preserveAspectRatio=True,anchor='ne')
    except Exception: pass
    # veu para o texto respirar por cima da foto
    c.setFillColor(Color(20/255,17/255,16/255,0.55)); c.rect(0,H-128*mm,W*0.72,128*mm,fill=1,stroke=0)
    c.restoreState()

    wordmark(c,M,H-24*mm,15,on_dark=True)
    c.setFillColor(WA(.50)); c.setFont('Ins',8.6)
    c.drawString(M,H-31*mm,"Limerick, Ireland")

    c.setFillColor(PINKB); c.roundRect(M,H-48*mm,25*mm,1.8*mm,0.9*mm,fill=1,stroke=0)
    c.setFillColor(HexColor("#FFFFFF")); c.setFont('Bri',33)
    c.drawString(M,H-66*mm,"How to rebuild")
    c.drawString(M,H-81*mm,"a ")
    grad_word(c,M+c.stringWidth("a ",'Bri',33),H-81*mm,"derelict house.",'Bri',33,PINK,GOLD)

    c.setFillColor(WA(.65)); c.setFont('Ins',10.5)
    c.drawString(M,H-96*mm,"Choosing the property, paying for it, and claiming the grant.")

    # assinatura da autora, dentro do bloco escuro
    c.setFillColor(WA(.08)); c.roundRect(M,H-119*mm,86*mm,14*mm,7*mm,fill=1,stroke=0)
    c.setFillColor(HexColor("#FFFFFF")); c.setFont('BriSB',11)
    c.drawString(M+8*mm,H-113.6*mm,"Written by Nina Chagas")
    c.setFillColor(WA(.50)); c.setFont('Ins',8)
    c.drawString(M+8*mm,H-117.6*mm,"who did it three times before writing it down")

    # indice
    y=H-152*mm
    for n,t in [("01","Choosing a property to buy and rent"),
                ("02","Different ways to buy in Ireland"),
                ("03","The Vacant Property Refurbishment Grant")]:
        c.setFillColor(GOLDD); c.setFont('Bri',16); c.drawString(M,y,n)
        c.setFillColor(INK);   c.setFont('BriSB',11.5); c.drawString(M+15*mm,y,t)
        c.setStrokeColor(LINE); c.setLineWidth(0.7); c.line(M,y-5.5*mm,W-M,y-5.5*mm)
        y-=15*mm

    c.setFillColor(SOFT); c.setFont('Ins',7.8)
    c.drawString(M,21*mm,"General information, not financial, legal or tax advice.")
    c.drawString(M,17*mm,"Rules and figures change. Confirm current requirements with the relevant authority before you act.")

def chrome(c,d):
    bg(c)
    c.setFillColor(PINKB); c.rect(0,H-8.5*mm,W,8.5*mm,fill=1,stroke=0)
    c.setFillColor(HexColor("#FFFFFF")); c.setFont('BriSB',7.6)
    c.drawString(M,H-5.8*mm,"OLD TO GOLD")
    c.setFont('Ins',7.4); c.setFillColor(WA(.75))
    c.drawRightString(W-M,H-5.8*mm,"How to rebuild a derelict house")
    c.setStrokeColor(LINE); c.setLineWidth(0.7); c.line(M,14.5*mm,W-M,14.5*mm)
    c.setFillColor(SOFT); c.setFont('Ins',7.4)
    c.drawString(M,10*mm,"Nina Chagas  ·  Old to Gold  ·  contact@oldtogold.ie")
    c.setFillColor(PINKD); c.setFont('BriSB',8.5)
    c.drawRightString(W-M,10*mm,str(c.getPageNumber()-1))

F=[]; A=F.append

# ══ A AUTORA ══════════════════════════════════════════════════════════
PW=62*mm
photo=Image(os.path.join(A_DIR,'nina-portrait.jpg'),width=PW,height=PW*1719/1294)
photo.hAlign='LEFT'

BIOW=FW-PW-9*mm-12
bio=[P("The person who wrote this",h1),
     P("I did not learn this from a course. I learned it by buying houses nobody else wanted, in Limerick, with my own money on the line.",lead),
     P("I moved from Brazil to Ireland at eighteen. I have spent more than 21 years here, graduated from the University of Limerick in 2020, and took my first step into property at the end of 2022. Since then I have bought and rebuilt three houses, applied for the Vacant Property Refurbishment Grant and been approved, and let the finished properties as long-term rentals.",body),
     P("Everything in this guide is a decision I have actually had to make. The order of the steps is the order I go in. The warnings are the things that cost me time or money the first time round. Where I am unsure, I say so, and I tell you who to ask instead.",body),
     Spacer(1,6),
     card([P("I am not selling you a strategy I read about. I am writing down the one I run.",pull)],bg=SAND,pad=13,width=BIOW)]

_t=Table([[photo,'',bio]],colWidths=[PW,9*mm,BIOW],hAlign='LEFT')
_t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
    ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
A(_t)
A(Spacer(1,12))
A(cards_row([
    [P("21",num),P("years in Ireland",cardb)],
    [P("2020",num),P("graduated, University of Limerick",cardb)],
    [P("3",num),P("houses bought and rebuilt",cardb)],
    [P("€70,000",S(name='n2',fontName='Bri',fontSize=20,leading=24,textColor=INK)),
     P("refurbishment grant approved",cardb)],
], bg=SAND, pad=12, rowh=30*mm))
A(Spacer(1,16))
A(P("The three houses this came from",h2))
A(Spacer(1,3))
A(cards_row([
    [P("Kileely Villas",cardt),P("Bought for €145,000, rebuilt for €186,129, now let at €3,000 a month. Completed.",cardb)],
    [P("Adelaide Terrace",cardt),P("€230,000 purchase, €150,000 refurbishment estimated, valued at €317,200. In progress.",cardb)],
    [P("Maryfield",cardt),P("Bought and about to start. The figures go on the website once the schedule is signed off.",cardb)],
], rowh=36*mm))
A(CondPageBreak(200*mm))

# ══ 01 ════════════════════════════════════════════════════════════════
A(P("Choosing a property to buy and rent",h1))
A(P("Finding the right property is about more than finding a cheap house.",lead))
A(P("Buying a property to rent is not simply about finding the lowest purchase price. A property can look like a bargain on paper and become an expensive mistake if the location is wrong, the refurbishment costs are underestimated, the rental income does not support the investment, or there are planning, structural or legal issues nobody identified before purchase.",body))
A(P("I look at the whole investment picture before deciding whether a property is right. My focus is on houses that have been vacant, neglected or need significant refurbishment, because that is where value can still be created through the right renovation and long-term management.",body))

A(P("Step 1. Start with the end goal",h2))
A(P("Before looking at individual properties, ask what you are trying to achieve. In my case the objective is to buy, refurbish, rent and hold as a long-term investment. That means knowing what the finished property should look like before deciding what you are prepared to pay for it.",body))
A(P("What I work out first",h3))
for x in UL([
 "What type of tenant am I trying to attract?",
 "What type of property is in demand in the area?",
 "What rent could the finished property realistically achieve?",
 "How much refurbishment will be required?",
 "What will the property be worth once the work is completed?",
 "How much capital can I invest, and what financing is available?",
 "What will the ongoing costs be, and will the return be acceptable?"]): A(x)
A(Spacer(1,3))
A(card([P("The purchase price is only one part of the calculation.",pull)],bg=SAND,pad=13))

A(P("Step 2. Choose the right location",h2))
A(P("For a rental investment, location is critical. A beautiful property in the wrong location can be much harder to rent than a modest property in an area with strong and consistent rental demand.",body))
A(rows([
 ("Employment","Major employers, business parks, hospitals or universities nearby."),
 ("Transport","How easily tenants reach public transport, roads and key destinations."),
 ("Education","Schools, colleges and universities within reach."),
 ("Amenities","Shops, supermarkets, healthcare, parks and everyday facilities."),
 ("Rental demand","Whether similar properties in the area are being let quickly."),
 ("Tenant profile","Who is likely to rent it. A young professional and a family want different things."),
 ("Future development","Planned developments or infrastructure that could affect the area either way."),
],head=("Factor","What I look at")))
A(Spacer(1,7))
A(card([P("I do not just ask whether I can buy the property cheaply. I ask whether people will want to live there.",pull)],bg=SAND,pad=13))

A(P("Step 3. Establish the realistic rental income",h2))
A(P("Before buying, you need to understand what the property could realistically rent for after refurbishment. Compare similar properties in the local market and account for size, number of bedrooms and bathrooms, condition, BER rating, quality of the refurbishment, parking, garden or outdoor space, transport links and location.",body))
A(P("Ireland's rent rules affect the answer",h3))
A(P("Since 1 March 2026, national rent-control rules apply to private tenancies, with specific rules governing rent increases and when a new tenancy can be set at market rent. The RTB also requires landlords to use appropriate market evidence when setting rent in circumstances where market rent can be applied.",body))
A(P("So an investment decision cannot rest on what you hope the property will rent for. The numbers have to work within the rules that actually apply to that property. Confirm the current position with the RTB before you commit.",body))

A(P("Step 4. Look beyond the purchase price",h2))
A(P("A property advertised at €180,000 is not necessarily a €180,000 investment. Before deciding what it really costs, add up everything that has to be paid before the first tenant moves in.",body))
A(rows([
 ("Purchase price","What you agree to pay, not the asking price."),
 ("Overbidding","Anything paid above affordability because of competition."),
 ("Stamp duty","Plus the other acquisition costs."),
 ("Legal fees","Solicitor and conveyancing."),
 ("Survey","Surveyor or engineer reports."),
 ("Mortgage protection","Where the lender requires it."),
 ("Planning","Where the works need it."),
 ("Refurbishment","The works themselves, with a contingency."),
],head=("Cost","Note")))
A(CondPageBreak(120*mm))

# ══ 02 ════════════════════════════════════════════════════════════════
A(P("Different ways to buy a property in Ireland",h1))
A(P("There is more than one way to finance a purchase. For most people the common route is a mortgage from a bank or other lender. Depending on your circumstances there are others: your own savings, investment partners, inheritance, selling another asset, or raising finance against a property you already own.",body))
A(P("The right option depends on your income, financial position, available capital, credit history, the type of property and what you intend to do with it. Before deciding, understand not only how much money you can access but what that money costs and how it affects the investment.",body))

A(P("1. A cash purchase",h2))
A(P("The simplest option is buying with money you already have. No mortgage application, no interest, no monthly repayments, a faster transaction, a stronger position when negotiating, and more control over the property.",body))
A(P("Buying with cash still has costs",h3))
A(P("Stamp duty, solicitor and conveyancing costs, survey and professional fees, refurbishment, insurance, ongoing maintenance and any other applicable purchase costs all remain.",body))
A(card([P("If you spend all your savings on the purchase, you may have very little left for refurbishment, emergencies or the unexpected. On an investment property, cash reserves matter as much as the purchase price.",pull)],bg=SAND,pad=13))

A(P("2. A bank mortgage",h2))
A(P("Instead of paying the whole price yourself, you contribute part and borrow the rest. On a €300,000 property that might mean a €60,000 deposit from you and €240,000 from the lender, repaid over the agreed term with interest.",body))
A(P("What you can borrow depends on your income, financial commitments, credit history, the property and the lender's criteria. For an investment property the lending rules can differ from those for a home you intend to live in.",body))
A(cards_row([
 [P("What it gives you",cardt),
  P("You do not need the full price available. Leverage lets you acquire a larger asset, and your own capital can spread across more than one investment.",cardb)],
 [P("What you take on",cardt),
  P("Mortgage repayments, interest rates, vacancies and lost rent, maintenance, insurance, the unexpected, and changes in the property market.",cardb)],
]))
A(Spacer(1,7))
A(card([P("Borrowing creates an obligation. The investment has to stay viable even when things do not go to plan.",pull)],bg=SAND,pad=13))

A(P("3. Raising finance against a property you own",h2))
A(P("If you already own a property that has risen in value, you may be able to approach a lender about borrowing against that equity, subject to their assessment and criteria. The funds could go towards another purchase or project.",body))
A(rows([("Property value","€400,000"),("Outstanding mortgage","€150,000"),("Gross equity","€250,000")],
       head=("Worked example","Amount"),w1=52*mm))
A(Spacer(1,7))
A(P("Gross equity of €250,000 does not mean you can borrow €250,000. The lender will assess the property, your income, existing debt and affordability before deciding what, if anything, is available.",body))
A(CondPageBreak(120*mm))

# ══ 03 ════════════════════════════════════════════════════════════════
A(P("The Vacant Property Refurbishment Grant",h1))
A(P("Croí Cónaithe Towns Fund. What you need, in the order the council asks for it.",lead))
A(P("This is the part people find hardest, because the paperwork comes in two waves: once to get approved, and again after the work is finished to actually get paid. What follows is the sequence I went through.",body))

A(P("First wave. Getting approved",h2))
A(rows([
 ("Application form","The proposed works you intend to carry out, with the cost stated for each one."),
 ("Quotation","From the contractor or supplier."),
 ("Engineering report","On the condition of the property."),
 ("Proof of ownership","Solicitor letter, plus the Revenue stamp certificate."),
 ("Proof of status","ESB letter showing the property is vacant, or a council letter showing it is derelict."),
],head=("Document","Detail")))
A(Spacer(1,8))
A(P("What the approval letter ties you to",h3))
A(P("Approval runs from the date of issue and is valid for a limited period, so the works have to be planned around that window. The conditions typically include a final site inspection of the completed works by the local authority, proof of ownership before drawdown, compliance with all relevant planning and building regulations, a legal charge over the property as security for the grant, and the clawback provisions below.",body))
A(P("For a rental property specifically, you must make the property available for rent and register the tenancy with the RTB before drawdown, and ensure it complies with fire safety and minimum standards regulations.",body))

A(P("Clawback. The condition people miss",h2))
A(P("The grant is repayable if the property changes use or is sold inside the clawback period. That period runs from the date the funding is transferred, not from approval.",body))
A(rows([
 ("Within 5 years","100% of the grant is repayable"),
 ("Over 5 and up to 10 years","75% of the grant is repayable"),
 ("Over 10 years","No clawback applies"),
],head=("Sold, or ceases to be a home or an RTB-registered rental","Clawback"),w1=88*mm))
A(Spacer(1,8))
A(card([P("A grant is not free money if you might sell in year three. Decide the holding period before you apply.",pull)],bg=SAND,pad=13))

A(P("Second wave. Getting paid after the works",h2))
A(P("Once the refurbishment is finished, the council needs the full evidence trail before releasing funds.",body))
A(rows([
 ("1. Cost breakdown","The completed works by category, with the cost of each."),
 ("2. Supplier and payment setup","The council's supplier and payment details form."),
 ("3. Invoice summary sheet","Every invoice numbered, with contractor, date and amount, and tax clearance attached for each one."),
 ("4. Proof of payment","Bank statements with the payments to contractors highlighted and identified, all receipts, and copies of any cheques issued."),
],head=("Step","What it contains")))
A(Spacer(1,8))
A(P("Which works count",h3))
A(P("The cost breakdown is organised by category. Demolition, strip out and site clearance including removal of hazardous waste. Substructure works including foundations, rising walls, floor slabs, damp-proofing and underpinning. Structural works to the superstructure including walls, party walls, chimneys, suspended timber floors and structural timbers. Internal walls, stairs and landings, including doors, windows and applied finishes. External wall completions including doors, windows, sills and applied finishes. Roof completions including flashings, fascia, soffits, gutters and downpipes. Building services: plumbing, heating, ventilation, electrical and telecommunications. Painting and decoration required because of the works carried out. An extension within the ambit of exempt development, as part of a wider refurbishment. Necessary external and site development works within the curtilage. Professional services associated with the works.",body))
A(P("Also required before payment",h3))
for x in UL([
 "Tax clearance certificate for every contractor supplying goods or services over €10,000.",
 "Confirmation from Revenue that Local Property Tax is paid up to date.",
 "Evidence of home insurance, with the policy updated to reflect the rental value if you applied as a rental.",
 "SEAI confirmation, by letter or email, that the grant-funded works received no funding from them, quoting the MPRN and the property address.",
]): A(x)
A(Spacer(1,5))
A(P("When all the documentation is approved you receive an appointment for the property inspection, and after that confirmation by email that payment is coming. Payments are made on Fridays.",body))

A(P("Plan for six months, or longer",h2))
A(P("The overall process may take six months or more. Do not make commitments or give anyone a specific repayment date based on the grant, because there is no guaranteed timeline for when the funds arrive. Build the delay into your cash flow from the start.",body))
A(CondPageBreak(105*mm))

# ══ FECHO ═════════════════════════════════════════════════════════════
A(KeepTogether([
  P("Where to go from here",h1),
  P("I am not a consultant. I buy these houses myself, and everything above is what I learned doing it. If you are working on a property in Limerick and something here does not match what you are being told, write to me and ask.",lead),
  Spacer(1,4),
  cards_row([
    [P("Talk to me",cardt),P("contact@oldtogold.ie",cardb)],
    [P("See the real figures",cardt),P("Three houses in Limerick, costs published in full",cardb)],
    [P("If you own a property",cardt),P("Ask about Rent-to-Rent and hand over the management",cardb)],
  ],bg=SAND,pad=12),
  Spacer(1,14),
  Rule(),
  P("Nina Chagas",S(name='sig',fontName='Bri',fontSize=16,leading=20,textColor=INK)),
  P("Founder, Old to Gold. Limerick, Ireland.",small),
  Spacer(1,8),
  P("This guide is general information based on my own experience in Limerick. It is not financial, legal, tax or planning advice, and it is not a recommendation to invest. Grant terms, tenancy rules and lending criteria change, and they vary by property and by local authority. Confirm the current requirements with the relevant authority, and take advice from a qualified professional, before you commit money. Old to Gold accepts no liability for decisions taken on the basis of this document.",small),
]))

doc=BaseDocTemplate(OUT,pagesize=A4,leftMargin=M,rightMargin=M,
    topMargin=17*mm,bottomMargin=19*mm,
    title="How to rebuild a derelict house",author="Nina Chagas, Old to Gold",
    subject="Choosing a property, paying for it, and claiming the Vacant Property Refurbishment Grant")
doc.addPageTemplates([
    PageTemplate(id='cover',frames=[Frame(M,19*mm,FW,H-36*mm,id='c')],onPage=cover),
    PageTemplate(id='body', frames=[Frame(M,19*mm,FW,H-17*mm-19*mm,id='n')],onPage=chrome),
])
F.insert(0,PageBreak())
F.insert(0,NextPageTemplate('body'))
doc.build(F)
print("gerado:",OUT)

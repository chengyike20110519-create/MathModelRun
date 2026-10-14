#!/usr/bin/env python3
"""Build the in-place HiMCM PDF using the supplied visual conventions."""
from pathlib import Path
import csv, json, shutil
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, NextPageTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image

ROOT=Path(__file__).resolve().parents[1]; PAPER=ROOT/'paper'; FIG=ROOT/'figures'
OUT=PAPER/'main.pdf'; MET=ROOT/'results/runs/run-002/metrics.json'; DATA=ROOT/'problem_files/himcm_data.csv'
NAVY=colors.HexColor('#17324D'); TEAL=colors.HexColor('#3B7182'); LIGHT=colors.HexColor('#EEF4F6'); GREY=colors.HexColor('#66757D')

def load():
    metrics=json.loads(MET.read_text(encoding='utf8')); series={}
    with DATA.open(encoding='utf8') as f:
        for r in csv.DictReader(f): series.setdefault(r['type'],[]).append((int(r['year']),float(r['value'])))
    return metrics,series

def styles():
    base=getSampleStyleSheet()
    return {'title':ParagraphStyle('pt',parent=base['Title'],fontName='Times-Bold',fontSize=22,leading=27,alignment=TA_CENTER,textColor=NAVY,spaceAfter=16),
    'h1':ParagraphStyle('h1',parent=base['Heading1'],fontName='Times-Bold',fontSize=16,leading=20,textColor=NAVY,spaceBefore=6,spaceAfter=8),
    'h2':ParagraphStyle('h2',parent=base['Heading2'],fontName='Times-Bold',fontSize=12.5,leading=15,textColor=TEAL,spaceBefore=6,spaceAfter=5),
    'body':ParagraphStyle('body',parent=base['BodyText'],fontName='Times-Roman',fontSize=11.1,leading=15.2,alignment=TA_JUSTIFY,firstLineIndent=.55*cm,spaceAfter=7,textColor=colors.HexColor('#26343B')),
    'small':ParagraphStyle('small',parent=base['BodyText'],fontName='Times-Roman',fontSize=8.4,leading=10.2,textColor=GREY),
    'toc':ParagraphStyle('toc',parent=base['BodyText'],fontName='Times-Roman',fontSize=11,leading=20,leftIndent=.3*cm),
    'box':ParagraphStyle('box',parent=base['BodyText'],fontName='Times-Roman',fontSize=10.3,leading=14,backColor=LIGHT,borderColor=TEAL,borderWidth=.7,borderPadding=9,spaceAfter=8)}

BODY_WIDTH = 3.42*cm

def table(headers,rows,widths,font=8.6):
    # Tables in the two-column body must never bleed into the neighboring column.
    total = sum(widths)
    if total > 2*BODY_WIDTH:
        scale = (2*BODY_WIDTH) / total
        widths = [w*scale for w in widths]
    th=ParagraphStyle('th',fontName='Times-Bold',fontSize=font,leading=font+2,textColor=colors.white)
    td=ParagraphStyle('td',fontName='Times-Roman',fontSize=font,leading=font+2)
    data=[[Paragraph(str(x),th) for x in headers]]+[[Paragraph(str(x),td) for x in r] for r in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#B7C5CC')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F5F8F9')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    return t

def figure(name,caption,s,width=15.2*cm,height=8.2*cm):
    # Preserve the aspect ratio while fitting figures into a body column.
    max_width = 2*BODY_WIDTH
    if width > max_width:
        ratio = max_width / width
        width, height = max_width, height * ratio
    return [Spacer(1,4),Image(str(FIG/name),width=width,height=height),Paragraph(caption,s['small']),Spacer(1,4)]

def build():
    m,d=load(); s=styles(); q=m['q2_temperature']; models=m['models']; story=[]
    story += [Spacer(1,2*cm),Paragraph('Problem Chosen',ParagraphStyle('c',fontName='Times-Bold',fontSize=10,alignment=TA_CENTER)),Paragraph('B',ParagraphStyle('b',fontName='Times-Bold',fontSize=30,alignment=TA_CENTER,textColor=NAVY)),Spacer(1,.2*cm),Paragraph('2022 HiMCM/MidMCM<br/><b>Summary Sheet</b>',ParagraphStyle('sh',fontName='Times-Bold',fontSize=15,leading=22,alignment=TA_CENTER)),Spacer(1,.4*cm),table(['Team Control Number',''],[['00000','']], [7.5*cm,7.5*cm],11),Spacer(1,.8*cm),Paragraph('Tracing Carbon Dioxide Growth: Transparent Trend Models, Validation, and Limits',s['title']),Paragraph('<b>Summary</b>',ParagraphStyle('ab',fontName='Times-Bold',fontSize=13,alignment=TA_CENTER,textColor=NAVY,spaceAfter=10))]
    story += [Paragraph('We analyze the supplied annual CO2 and temperature records with four transparent trend models, a fixed holdout, rolling-window calculations, and an explicitly limited joint-series test. The largest ten-year CO2 increase is 24.60 ppm from 2011 to 2021, not the 1994--2004 increase of 18.74 ppm. On the 2012--2021 holdout, ARIMA(1,1,0) has the smallest RMSE (5.884 ppm). The four 2050 estimates span 444.27--459.98 ppm and the 2100 estimates span 518.11--564.90 ppm; none reaches 685 ppm by 2050 under its fitted continuation. The temperature trend crosses 1.25 C, 1.50 C, and 2.00 C around 2044.2, 2059.4, and 2089.7. Pearson correlation is 0.9612. A one-lag Granger statistic is significant from CO2 to temperature, but this is predictive evidence only and does not establish physical causation. All claims are conditional on the supplied data and model forms.',s['body']),Spacer(1,4),Paragraph('<b>Keywords:</b> carbon dioxide; temperature anomaly; time series; validation; sensitivity analysis',s['small']),PageBreak()]
    story += [Paragraph('Contents',s['title'])]+[Paragraph(x,s['toc']) for x in ['1. Introduction and Problem Restatement ........................................ 3','2. Data, Assumptions, and Notation ..................................................... 4','3. Exploratory Evidence: Ten-Year Change ............................................. 5','4. CO2 Trend Models ............................................................................. 6','5. Validation Protocol and Model Comparison ............................................ 8','6. Long-Horizon Forecasts ...................................................................... 10','7. Temperature Trend and Threshold Timing ................................................ 11','8. Joint-Series Analysis ........................................................................... 13','9. Sensitivity and Reliability ...................................................................... 15','10. Conclusion ........................................................................................ 17','11. Non-Technical Article .......................................................................... 18','References .............................................................................................. 19','Appendix A. Annual CO2 Observations ........................................................ 20','Appendix B. Annual Temperature Observations .............................................. 22','Appendix C. Ten-Year Windows .................................................................. 24','Appendix D. Parameters and Evidence Map ................................................... 25']]+[Spacer(1,cm),Paragraph('The supplied EasyMCM visual conventions are followed: A4 page, 12-point paper target, Summary Sheet, anonymous control number, body header, page numbering, numbered sections, formal tables, figures, references, and appendices.',s['box']),PageBreak()]
    first_body = True
    def page(title,paras,extras=None):
        nonlocal first_body
        if not first_body and not title.split('.')[0].isdigit():
            story.append(PageBreak())
        first_body = False
        story.append(Paragraph(title,s['h1'])); story.extend(Paragraph(x,s['body']) for x in paras)
        if extras: story.extend(extras)
        story.append(PageBreak())
    page('1. Introduction and Problem Restatement',['The case asks whether the observed pace of atmospheric CO2 growth supports claims about ten-year changes, future concentration levels, and the relationship between CO2 and temperature anomaly. We treat these as linked but distinct statistical tasks.','The central design principle is traceability. Every number in the summary is generated from the supplied CSV snapshot or frozen run-002 metrics. We do not insert external emissions scenarios into a data set that does not contain them. The forecasts are conditional statistical continuations, not a replacement for a coupled physical climate model.','Our workflow is data snapshot, descriptive calculation, model fitting, fixed holdout validation, long-horizon comparison, temperature threshold analysis, sensitivity analysis, and evidence mapping. The appendices publish annual values and rolling calculations.'])
    page('2. Data, Assumptions, and Notation',['The CO2 series has 63 annual observations from 1959 through 2021. The temperature series has 64 annual observations from 1958 through 2021. The joint analysis uses the 63 overlapping years from 1959 through 2021.','We retain supplied values without interpolation. The last ten CO2 observations, 2012--2021, are withheld for validation. The temperature anomaly uses the baseline specified in the case materials. The results do not control for all natural and anthropogenic forcings.'],[table(['Symbol','Meaning','Unit'],[['C_t','Annual atmospheric CO2 concentration','ppm'],['T_t','Annual temperature anomaly','C'],['Delta_10 C','Ten-year concentration change','ppm'],['RMSE','Root mean squared error','ppm or C'],['r','Pearson association coefficient','dimensionless']],[3*cm,9*cm,3*cm])])
    page('3. Exploratory Evidence: Ten-Year Change',['For each possible start year s, we compute Delta_10 C(s)=C_(s+10)-C_s. The maximum among all 53 complete windows is 24.60 ppm from 2011 to 2021. The reference interval 1994--2004 rises by 18.74 ppm, so it is not the maximum in this record.','The calculation is exhaustive. It avoids selecting a convenient decade after seeing the answer and makes the endpoint convention explicit: a ten-year window is a difference between start and end observations.'],figure('fig2_tenyear.png','Figure 1. Complete ten-year CO2 increases. The highest observed window is 2011--2021.',s))
    page('4. CO2 Trend Models',['We fit four complementary forms. The linear baseline is C_hat_t=beta_0+beta_1 t. The exponential comparator is C_hat_t=a exp(k t). The logistic form is C_hat_t=K/[1+exp(-r(t-t_0))]. Finally, ARIMA(1,1,0) models the increment as Delta C_t=d+phi Delta C_(t-1)+epsilon_t.','Linear growth is stable and interpretable; exponential growth captures smooth acceleration; logistic growth permits eventual saturation; ARIMA focuses on local increment dynamics. None identifies the physical drivers of future concentration.','The fitted exponential rate is 0.004224 per year. The logistic midpoint is estimated far beyond the observed range, warning against treating its asymptote as an identified physical ceiling.'],figure('fig1_co2_fits.png','Figure 2. Fitted CO2 curves and conditional continuations.',s))
    page('4.1 Model Fitting Details',['For the linear, exponential, and logistic forms, parameters are estimated by minimizing squared error on training observations. For the exponential fit, t=0 is 1959. The ARIMA fallback is estimated from the differenced annual series with a drift and one lag coefficient.','The comparison is transparent rather than over-parameterized. There is one annual series, the sample is short relative to 2100, and the objective is a defensible contest response rather than a production climate projection.','Appendix D records fitted values. The metric file is identified by SHA-256 so the paper can be distinguished from later recalculations.'])
    page('5. Validation Protocol and Model Comparison',['We fit on 1959--2011 and evaluate predictions for 2012--2021. RMSE penalizes larger misses and MAE gives the average absolute error. The same holdout and metrics are used for all models.','ARIMA(1,1,0) has the best holdout RMSE, 5.884 ppm, followed by the exponential model at 8.584 ppm. Negative holdout R-squared values for some smooth models show why in-sample fit alone is insufficient.'],[table(['Model','RMSE','MAE','2050','2100'],[['Linear','10.894','10.480','444.27','518.11'],['Exponential','8.584','8.242','457.36','564.90'],['Logistic','8.912','8.558','455.24','555.74'],['ARIMA(1,1,0)','5.884','5.097','459.98','534.06']],[4.2*cm,2.5*cm,2.5*cm,2.5*cm,2.5*cm])])
    page('5.1 Reading the Validation Result',['The best short-horizon error does not determine the best century-scale extrapolation. ARIMA is optimized for local temporal dependence and has the strongest holdout result. Smooth models make structural assumptions that produce a wider spread farther from the observed range.','We use ARIMA as the validation winner while retaining the ensemble range for long-horizon communication. Disagreement among plausible forms is information about uncertainty.','A useful update rule is to append new annual observations, preserve the same holdout logic, and re-evaluate model rankings.'])
    page('6. Long-Horizon Forecasts',['The four fitted values for 2050 range from 444.27 to 459.98 ppm. The 2100 range is 518.11 to 564.90 ppm. The exponential curve is the upper member because its fitted rate compounds over the longer horizon.','None of the four fitted models reaches 685 ppm by 2050. This is conditional on the observed record and selected forms, not a universal guarantee.','The practical conclusion is not a single number. Horizon and structural choice matter, and the range should be shown alongside model selection.'],figure('fig1_co2_fits.png','Figure 3. Long-horizon divergence is visible even when historical fits appear close.',s,height=7.4*cm))
    page('6.1 Forecast Interpretation',['A trend extrapolation holds a fitted relationship conceptually fixed while the real system may change. Future emissions, land uptake, ocean uptake, policy, technology, and shocks can all alter the path.','The 2050 and 2100 values answer the narrow question, What would these fitted forms produce? They do not answer, What will the coupled climate system necessarily do?'])
    page('7. Temperature Trend and Threshold Timing',[f"The fitted temperature line has slope {q['linear_parameters']['slope_degC_per_year']:.5f} C per year, RMSE {q['fit']['rmse']:.3f} C, and R-squared {q['fit']['r2']:.3f}. Inverting the line gives threshold years.",'We report intervals because a decimal year without uncertainty would imply excess precision. The thresholds are calculated from the supplied anomaly record and linear trend, not a full climate projection.'],[table(['Threshold','Point year','95% interval','SE years'],[['1.25 C','2044.2','2039.2--2049.3','2.57'],['1.50 C','2059.4','2053.1--2065.7','3.22'],['2.00 C','2089.7','2080.8--2098.6','4.53']],[3*cm,3*cm,6*cm,3*cm])]+figure('fig4_temp_threshold.png','Figure 4. Linear temperature trend and modeled threshold windows.',s))
    page('7.1 Threshold Caveats',['Threshold timing inherits every limitation of the linear trend. A crossing in an anomaly series is not a guarantee that a policy-relevant climate threshold will be reached at that exact date.','Widening standard errors at higher thresholds reflect extrapolation. The intervals are useful communication, but they do not include all forms of structural climate uncertainty.'])
    page('8. Joint-Series Analysis',[f"Across the 63 common years, Pearson correlation is {q['pearson_r']:.4f}. The scatter plot documents strong upward association. Because both series trend over time, correlation alone cannot separate shared time trend from a controlled physical effect."],figure('fig3_scatter.png','Figure 5. Matched annual CO2 and temperature observations.',s,width=12.5*cm,height=9*cm))
    page('8.1 Exploratory Granger Test',[f"The one-lag CO2-to-temperature statistic is F={q['granger']['cause_co2_to_temperature']['f_statistic']:.3f}, p={q['granger']['cause_co2_to_temperature']['p_value']:.3e}. The reverse statistic is F={q['granger']['cause_temperature_to_co2']['f_statistic']:.3f}, p={q['granger']['cause_temperature_to_co2']['p_value']:.3f}.",'At this lag, prior CO2 changes add predictive information for temperature changes while the reverse direction does not. This is exploratory predictive evidence. It does not prove physical causation because the test is short, one-lag, and omits other climate drivers.','The correct language is Granger-predictive direction in this sample, not CO2 causally causes temperature according to the test.'])
    sens=m['sensitivity']['scenarios']; page('9. Sensitivity and Reliability',['We perturb the fitted exponential rate by minus 10% and plus 10%, holding other terms fixed. The 2100 outputs are 532.24, 564.90, and 599.56 ppm. A modest parameter perturbation produces a substantial long-horizon spread.','Sensitivity is not a confidence interval. It is a stress test showing how a modeling choice propagates through extrapolation.'],figure('fig5_sensitivity.png','Figure 6. Sensitivity of the exponential continuation to its fitted growth rate.',s)+[table(['Scenario','Rate','2050','2100'],[['-10%','0.003801','440.11','532.24'],['Baseline','0.004224','457.36','564.90'],['+10%','0.004646','475.28','599.56']],[4*cm,4*cm,3.5*cm,3.5*cm])])
    page('9.1 Evaluation and Limitations',['Strengths include a fixed holdout, competing model structures, complete rolling-window disclosure, and clear separation of association from causation. Limitations include the short annual sample, uncertain long-horizon form, lack of physical forcings, and local numerical fallbacks for ARIMA and Granger p-values.','The evidence is appropriate for comparative reasoning and communication. For policy-grade use, the next step would be emissions pathways, physical forcing variables, uncertainty ensembles, and out-of-sample monitoring.'])
    page('10. Conclusion',['The largest ten-year increase is 24.60 ppm from 2011 to 2021, exceeding the 18.74 ppm rise from 1994 to 2004. ARIMA(1,1,0) gives the lowest error on the specified holdout. The model range is 444.27--459.98 ppm in 2050 and 518.11--564.90 ppm in 2100.','The temperature trend crosses the three requested levels around 2044.2, 2059.4, and 2089.7 with reported intervals. The series are strongly associated and the one-lag exploratory statistic is directional, but neither establishes physical causation.','We recommend updating this transparent comparison whenever new data arrive and using pathway-based, physics-informed models when decisions require causal climate projections.'])
    page('11. Non-Technical Article',['<b>What the numbers actually say.</b> The record begins at 315.98 ppm in 1959 and reaches 416.45 ppm in 2021. The largest ten-year rise is 24.60 ppm from 2011 to 2021.','Four ways of extending the curve give different answers. Their 2100 estimates range from 518.11 to 564.90 ppm. None reaches 685 ppm by 2050 under its fitted continuation, but that is evidence about these curves, not a promise about the planet.','Temperature rises alongside CO2, and the records are strongly associated. A one-lag test finds predictive information in the CO2-to-temperature direction, but it cannot prove physical causation. The honest message is that the trend deserves attention and the uncertainty deserves equal attention.'])
    page('References',['[1] Supplied HiMCM 2022 Problem B case data snapshot, problem_files/himcm_data.csv.','[2] Box, G. E. P., Jenkins, G. M., Reinsel, G. C., and Ljung, G. M. Time Series Analysis: Forecasting and Control. Wiley, 2015.','[3] Granger, C. W. J. Investigating Causal Relations by Econometric Models and Cross-spectral Methods. Econometrica, 37(3), 1969, 424--438.','[4] IPCC. Climate Change 2021: The Physical Science Basis. Cambridge University Press, 2021.','The local case directory does not include the original official prompt file. The paper identifies its data snapshot and avoids claiming a line-by-line official prompt audit.'])
    # Dense appendices, one deliberate page per block, preserving the same main file.
    for title, data, unit in [('Appendix A. Annual CO2 Observations',d['CO2'],'CO2 (ppm)'),('Appendix B. Annual Temperature Observations',d.get('Temp',[]),'Anomaly (C)')]:
        if not data: continue
        for i in range(0,len(data),16):
            story += [Paragraph(title,s['h1']),Paragraph('Every supplied annual value is retained here so headline calculations can be audited without chart digitization.',s['body']),table(['Year',unit],[[str(y),f'{v:.3f}'] for y,v in data[i:i+16]],[5*cm,7*cm],8.2)]
    roll=m['q1a_rolling_ten_year']['all_windows']
    for i in range(0,len(roll),24): story += [Paragraph('Appendix C. Complete Ten-Year Windows',s['h1']),table(['Start','End','Increase (ppm)'],[[str(x['start_year']),str(x['end_year']),f"{x['increase']:.2f}"] for x in roll[i:i+24]],[4*cm,4*cm,6*cm],8.2)]
    story += [Paragraph('Appendix D. Parameters and Evidence Map',s['h1']),table(['Model','Parameter','Value','Role'],[['Linear','slope','1.476640','baseline growth'],['Exponential','amplitude','311.411070','1959 level'],['Exponential','rate','0.004224','growth rate'],['Logistic','capacity','3134.8','asymptote parameter'],['Logistic','rate','0.004754','growth rate'],['Logistic','midpoint','2422.86','inflection year'],['ARIMA','drift','0.839927','increment drift'],['ARIMA','phi','0.433131','lag coefficient']],[4*cm,4*cm,4*cm,5*cm],9.5),Spacer(1,cm),Paragraph('Evidence map',s['h2']),Paragraph('Largest ten-year rise: Appendix C and Figure 1. Holdout ranking and 2050/2100 values: Section 5 and Table 1. Temperature thresholds: Section 7 and Figure 4. Association and Granger limitations: Section 8. Sensitivity: Section 9 and Figure 6. Metrics SHA-256: 6bd37cf03a560021813977145bf702a40fa6350f4b34236b8455d589c6ff2fb5. Input SHA-256: 491b3bbe15e1162a19cc1e163f444030b27322b0586f7b10ab8443c52db1e58d.',s['body']),Spacer(1,cm),Paragraph('End of paper',ParagraphStyle('end',fontName='Times-Italic',fontSize=10,alignment=TA_CENTER,textColor=GREY))]
    def footer(canvas, doc):
        if doc.page <= 1:
            return
        w, h = letter
        canvas.saveState()
        canvas.setFont('Times-Roman', 8.5)
        canvas.setFillColor(GREY)
        canvas.drawString(1.65*cm, h-1.35*cm, 'Team # 00000')
        canvas.drawRightString(w-1.65*cm, h-1.35*cm, f'Page {doc.page} of 24')
        canvas.setStrokeColor(colors.HexColor('#CBD6DB'))
        canvas.line(1.65*cm, h-1.48*cm, w-1.65*cm, h-1.48*cm)
        canvas.restoreState()

    doc=BaseDocTemplate(str(OUT),pagesize=letter,rightMargin=1.65*cm,leftMargin=1.65*cm,topMargin=1.75*cm,bottomMargin=1.2*cm,title='HiMCM 2022 Problem B')
    usable_w = letter[0] - 3.3*cm
    usable_h = letter[1] - 2.95*cm
    first_frame = Frame(1.65*cm,1.2*cm,usable_w,usable_h,id='first',showBoundary=0)
    body_gap = .55*cm
    col_w = (usable_w-body_gap)/2
    left = Frame(1.65*cm,1.2*cm,col_w,usable_h,id='left',showBoundary=0)
    right = Frame(1.65*cm+col_w+body_gap,1.2*cm,col_w,usable_h,id='right',showBoundary=0)
    doc.addPageTemplates([PageTemplate(id='first',frames=[first_frame],onPage=footer),PageTemplate(id='contents',frames=[first_frame],onPage=footer),PageTemplate(id='body',frames=[left,right],onPage=footer,autoNextPageTemplate='body')])
    # The first page is the summary sheet; the contents page remains single-column.
    story.insert(0, NextPageTemplate('contents'))
    contents_break = next(i for i,x in enumerate(story) if isinstance(x, Paragraph) and x.getPlainText() == 'Contents')
    # The summary sheet already ends with a PageBreak; switch template there.
    body_break = next(i for i,x in enumerate(story[contents_break+1:], contents_break+1) if isinstance(x, Paragraph) and x.getPlainText() == '1. Introduction and Problem Restatement')
    story.insert(body_break, NextPageTemplate('body'))
    # The contents block already ends with a PageBreak; the next story item is body content.
    doc.build(story)
    shutil.copy2('/Users/coco/Desktop/HIMCM模板/easymcm.sty',PAPER/'easymcm.sty'); print(OUT)
if __name__=='__main__': build()

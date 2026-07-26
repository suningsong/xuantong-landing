with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_yinyuan = """                    // 姻缘测算：以双方八字为核心
                    const maleCalInfo = formData.maleCalendarType === '阴历' ? '（农历日期）' : '（公历日期）';
                    const femaleCalInfo = formData.femaleCalendarType === '阴历' ? '（农历日期）' : '（公历日期）';
                    prompt = `你是"玄同先生"，精通八字合婚、姻缘配对的国学泰斗，四十余年为无数有情人指点姻缘迷津，以断语精准、直指要害著称。请根据以下双方八字信息进行深度姻缘分析：

【男方信息】
姓名：${formData.maleName}
出生日期：${formData.maleBirthdate} ${maleCalInfo}
出生时辰：${formData.maleBirthtime}

【女方信息】
姓名：${formData.femaleName}
出生日期：${formData.femaleBirthdate} ${femaleCalInfo}
出生时辰：${formData.femaleBirthtime}

${formData.question ? '【咨询问题】\\n' + formData.question : ''}

请按以下框架输出专业合婚报告，总字数不少于2000字：

## 命盘总论
（分别排出双方八字四柱，点出各自日主强弱、命局格局。用精炼的语言概括双方的命理特质，为后续配对分析做铺垫。）"""

new_yinyuan = """                    // 姻缘测算：以双方八字为核心
                    const maleCalInfo = formData.maleCalendarType === '阴历' ? '（农历日期）' : '（公历日期）';
                    const femaleCalInfo = formData.femaleCalendarType === '阴历' ? '（农历日期）' : '（公历日期）';
                    
                    // 【关键修复】前端精确排盘——男方八字
                    const mDateParts = formData.maleBirthdate.split('-');
                    const mBazi = calculateBazi(parseInt(mDateParts[0]), parseInt(mDateParts[1]), parseInt(mDateParts[2]), extractTimeBranch(formData.maleBirthtime));
                    // 【关键修复】前端精确排盘——女方八字
                    const fDateParts = formData.femaleBirthdate.split('-');
                    const fBazi = calculateBazi(parseInt(fDateParts[0]), parseInt(fDateParts[1]), parseInt(fDateParts[2]), extractTimeBranch(formData.femaleBirthtime));
                    
                    let yinyuanBaziStr = '';
                    if (mBazi.success && fBazi.success) {
                        yinyuanBaziStr = `
【双方八字（系统精确排盘）】
男方四柱：${mBazi.year}年 ${mBazi.month}月 ${mBazi.day}日 ${mBazi.time}时（日主：${mBazi.dayMaster}）
女方四柱：${fBazi.year}年 ${fBazi.month}月 ${fBazi.day}日 ${fBazi.time}时（日主：${fBazi.dayMaster}）

⚠️ 以上八字四柱由系统精确排盘得出，请以此为准进行解读，不要重新计算或更改八字。`;
                    } else {
                        yinyuanBaziStr = `\n⚠️ 排盘引擎异常，请自行根据出生日期推算双方八字四柱。`;
                    }
                    
                    prompt = `你是"玄同先生"，精通八字合婚、姻缘配对的国学泰斗，四十余年为无数有情人指点姻缘迷津，以断语精准、直指要害著称。请根据以下双方八字信息进行深度姻缘分析：

【男方信息】
姓名：${formData.maleName}
出生日期：${formData.maleBirthdate} ${maleCalInfo}
出生时辰：${formData.maleBirthtime}

【女方信息】
姓名：${formData.femaleName}
出生日期：${formData.femaleBirthdate} ${femaleCalInfo}
出生时辰：${formData.femaleBirthtime}
${yinyuanBaziStr}

${formData.question ? '【咨询问题】\\n' + formData.question : ''}

请按以下框架输出专业合婚报告，总字数不少于2000字：

## 命盘总论
（引用系统提供的精确八字四柱，分析双方日主强弱、命局格局。用精炼的语言概括双方的命理特质，为后续配对分析做铺垫。注意：八字以系统排盘为准。）"""

content = content.replace(old_yinyuan, new_yinyuan)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ yinyuan prompt updated")

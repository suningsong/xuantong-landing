import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add lunar-javascript CDN before the main <script> tag
cdn_script = '<script src="https://cdn.jsdelivr.net/npm/lunar-javascript@1.6.12/lunar.js"></script>'
old_script_tag = '    <script>'
content = content.replace(old_script_tag, f'    {cdn_script}\n{old_script_tag}', 1)

# 2. Add calculateBazi function right after the opening <script> tag
bazi_func = '''
        // ========= 八字精确排盘引擎 (基于 lunar-javascript) =========
        function calculateBazi(year, month, day, timeBranchChar) {
            try {
                const solar = Solar.fromYmd(year, month, day);
                const lunar = solar.getLunar();
                const eightChar = lunar.getEightChar();
                
                const result = {
                    yearGan: eightChar.getYearGan(),
                    yearZhi: eightChar.getYearZhi(),
                    monthGan: eightChar.getMonthGan(),
                    monthZhi: eightChar.getMonthZhi(),
                    dayGan: eightChar.getDayGan(),
                    dayZhi: eightChar.getDayZhi(),
                    timeGan: '',
                    timeZhi: timeBranchChar || '子'
                };
                
                // 计算时柱天干：五鼠遁时起时法
                // 甲己日起甲子时，乙庚日起丙子时，丙辛日起戊子时，丁壬日起庚子时，戊癸日起壬子时
                const dayGanIndex = '甲乙丙丁戊己庚辛壬癸'.indexOf(result.dayGan);
                const timeZhiIndex = '子丑寅卯辰巳午未申酉戌亥'.indexOf(result.timeZhi);
                
                let timeGanStartIndex;
                if ([0, 5].includes(dayGanIndex % 5)) {
                    // 甲/己日 → 子时起甲
                    timeGanStartIndex = 0;
                } else if ([1, 6].includes(dayGanIndex % 5)) {
                    // 乙/庚日 → 子时起丙
                    timeGanStartIndex = 2;
                } else if ([2, 7].includes(dayGanIndex % 5)) {
                    // 丙/辛日 → 子时起戊
                    timeGanStartIndex = 4;
                } else if ([3, 8].includes(dayGanIndex % 5)) {
                    // 丁/壬日 → 子时起庚
                    timeGanStartIndex = 6;
                } else {
                    // 戊/癸日 → 子时起壬
                    timeGanStartIndex = 8;
                }
                
                const tianGan = '甲乙丙丁戊己庚辛壬癸';
                result.timeGan = tianGan[(timeGanStartIndex + timeZhiIndex) % 10];
                
                return {
                    success: true,
                    year: result.yearGan + result.yearZhi,
                    month: result.monthGan + result.monthZhi,
                    day: result.dayGan + result.dayZhi,
                    time: result.timeGan + result.timeZhi,
                    full: result.yearGan + result.yearZhi + ' ' + result.monthGan + result.monthZhi + ' ' + result.dayGan + result.dayZhi + ' ' + result.timeGan + result.timeZhi,
                    dayMaster: result.dayGan,
                    lunar: '农历' + lunar.getYearInGanZhi() + '年' + lunar.getMonthInChinese() + '月' + lunar.getDayInChinese()
                };
            } catch(e) {
                console.error('八字排盘失败:', e);
                return { success: false, error: e.message };
            }
        }
        
        // 从时辰选择字符串中提取地支
        function extractTimeBranch(timeStr) {
            if (!timeStr) return '子';
            const branches = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
            for (const b of branches) {
                if (timeStr.includes(b)) return b;
            }
            return '子';
        }
        // ========= 排盘引擎结束 =========

'''
# Insert after the first <script> tag
content = content.replace('    <script>\n', '    <script>\n' + bazi_func, 1)

# 3. Modify the bazi/caiyun prompt to include pre-calculated 八字
# Find the section where bazi/caiyun prompt is constructed
old_bazi_section = """                    // 八字/财运：以出生信息为核心
                    const calendarInfo = formData.calendarType === '阴历' ? '（农历日期）' : '（公历日期）';
                    const isCaiyun = currentService === 'caiyun';
                    prompt = `你是"玄同先生"，国学泰斗，精研${serviceNames[currentService]}四十余载。请根据以下信息进行${isCaiyun ? '深度财运分析' : '全面命理推演'}。

【求测信息】
姓名：${formData.name}
性别：${formData.gender === 'male' ? '男' : '女'}
出生日期：${formData.birthdate} ${calendarInfo}
出生时辰：${formData.birthtime}
咨询问题：${formData.question || (isCaiyun ? '请深度分析财运格局' : '请全面分析运势')}"""

new_bazi_section = """                    // 八字/财运：以出生信息为核心
                    const calendarInfo = formData.calendarType === '阴历' ? '（农历日期）' : '（公历日期）';
                    const isCaiyun = currentService === 'caiyun';
                    
                    // 【关键修复】前端精确排盘，不依赖LLM计算八字
                    const baziDateParts = formData.birthdate.split('-');
                    const baziYear = parseInt(baziDateParts[0]);
                    const baziMonth = parseInt(baziDateParts[1]);
                    const baziDay = parseInt(baziDateParts[2]);
                    const baziTimeBranch = extractTimeBranch(formData.birthtime);
                    const baziResult = calculateBazi(baziYear, baziMonth, baziDay, baziTimeBranch);
                    
                    let baziInfoStr = '';
                    if (baziResult.success) {
                        baziInfoStr = `
【八字排盘（系统精确计算）】
四柱：${baziResult.year}年 ${baziResult.month}月 ${baziResult.day}日 ${baziResult.time}时
日主：${baziResult.dayMaster}
${baziResult.lunar}

⚠️ 以上八字四柱由系统精确排盘得出，请以此为准进行解读，不要重新计算或更改八字。`;
                    } else {
                        baziInfoStr = `\n⚠️ 排盘引擎异常，请自行根据出生日期推算八字四柱。`;
                    }
                    
                    prompt = `你是"玄同先生"，国学泰斗，精研${serviceNames[currentService]}四十余载。请根据以下信息进行${isCaiyun ? '深度财运分析' : '全面命理推演'}。

【求测信息】
姓名：${formData.name}
性别：${formData.gender === 'male' ? '男' : '女'}
出生日期：${formData.birthdate} ${calendarInfo}
出生时辰：${formData.birthtime}
咨询问题：${formData.question || (isCaiyun ? '请深度分析财运格局' : '请全面分析运势')}
${baziInfoStr}"""

content = content.replace(old_bazi_section, new_bazi_section)

# 4. Also update the "命盘总论" section to reference the pre-calculated Bazi
old_mingpan = """## 命盘总论
（排出八字四柱，点明日主强弱，概括命局格局——如正官格、偏财格、伤官配印等。用一两句话直击命主最核心的命运特征，让人一读就有"原来如此"的顿悟感。引用《滴天髓》或《穷通宝鉴》相关论述佐证。）"""

new_mingpan = """## 命盘总论
（引用系统提供的精确八字四柱，分析日主强弱，概括命局格局——如正官格、偏财格、伤官配印等。用一两句话直击命主最核心的命运特征，让人一读就有"原来如此"的顿悟感。引用《滴天髓》或《穷通宝鉴》相关论述佐证。注意：八字以系统排盘为准，不要自行推算。）"""

content = content.replace(old_mingpan, new_mingpan)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ bazi/caiyun prompt updated")

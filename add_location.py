with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============ 1. 添加城市经度数据库 + 真太阳时计算 ============
location_code = '''
        // ========= 城市经度数据库（用于真太阳时校正）=========
        const CITY_LONGITUDE = {
            // 东北
            '哈尔滨':126.6,'长春':125.3,'沈阳':123.4,'大连':121.6,
            // 华北
            '北京':116.4,'天津':117.2,'石家庄':114.5,'太原':112.5,'呼和浩特':111.7,
            // 华东
            '上海':121.5,'南京':118.8,'杭州':120.2,'苏州':120.6,'无锡':120.3,
            '合肥':117.3,'济南':117.0,'青岛':120.4,'福州':119.3,'厦门':118.1,
            '南昌':115.9,'宁波':121.5,'温州':120.7,'常州':119.9,'南通':120.9,
            // 华中
            '武汉':114.3,'长沙':113.0,'郑州':113.6,
            // 华南
            '广州':113.3,'深圳':114.1,'南宁':108.3,'海口':110.3,'东莞':113.7,
            '佛山':113.1,'珠海':113.5,'惠州':114.4,
            // 西南
            '成都':104.1,'重庆':106.5,'昆明':102.7,'贵阳':106.7,'拉萨':91.1,
            '绵阳':104.7,'德阳':104.4,'宜宾':104.6,'大理':100.2,
            // 西北
            '西安':108.9,'兰州':103.8,'西宁':101.8,'银川':106.3,'乌鲁木齐':87.6,
            '克拉玛依':84.9,'喀什':76.0,'哈密':93.5,'吐鲁番':89.2,
            // 其他
            '香港':114.2,'澳门':113.5,'台北':121.5,'高雄':120.3
        };
        
        // 省份默认经度（城市未知时使用省份近似值）
        const PROVINCE_LONGITUDE = {
            '北京':116.4,'天津':117.2,'河北':114.5,'山西':112.5,'内蒙古':111.7,
            '辽宁':123.4,'吉林':125.3,'黑龙江':126.6,'上海':121.5,'江苏':118.8,
            '浙江':120.2,'安徽':117.3,'福建':119.3,'江西':115.9,'山东':117.0,
            '河南':113.6,'湖北':114.3,'湖南':113.0,'广东':113.3,'广西':108.3,
            '海南':110.3,'重庆':106.5,'四川':104.1,'贵州':106.7,'云南':102.7,
            '西藏':91.1,'陕西':108.9,'甘肃':103.8,'青海':101.8,'宁夏':106.3,
            '新疆':87.6,'香港':114.2,'澳门':113.5,'台湾':121.0
        };
        
        // 根据城市名查找经度
        function getLongitude(cityName) {
            if (!cityName) return 120.0; // 默认东八区标准经度
            // 精确匹配城市
            for (const [city, lng] of Object.entries(CITY_LONGITUDE)) {
                if (cityName.includes(city) || city.includes(cityName)) return lng;
            }
            // 尝试匹配省份
            for (const [prov, lng] of Object.entries(PROVINCE_LONGITUDE)) {
                if (cityName.includes(prov) || prov.includes(cityName)) return lng;
            }
            return 120.0; // 未匹配到，使用标准经度
        }
        
        // 真太阳时校正：根据经度差计算时间偏移
        function getTrueSolarTime(timeStr, longitude) {
            // timeStr格式: "子时 (23:00-01:00)" 或类似
            const timeMatch = timeStr.match(/(\\d{1,2}):(\\d{2})/);
            if (!timeMatch) return { correctedTimeStr: timeStr, correctedBranch: null };
            
            let hours = parseInt(timeMatch[1]);
            let minutes = parseInt(timeMatch[2]);
            
            // 真太阳时校正：每度4分钟，东经120°为基准
            const correctionMinutes = Math.round((longitude - 120.0) * 4);
            let totalMinutes = hours * 60 + minutes + correctionMinutes;
            
            // 处理跨天
            if (totalMinutes < 0) totalMinutes += 1440;
            if (totalMinutes >= 1440) totalMinutes -= 1440;
            
            const correctedHours = Math.floor(totalMinutes / 60);
            const correctedMins = totalMinutes % 60;
            
            // 确定校正后的时辰地支
            const branches = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
            let branchIndex;
            if (correctedHours === 23 || correctedHours === 0) {
                branchIndex = 0; // 子时 23:00-01:00
            } else {
                branchIndex = Math.floor((correctedHours + 1) / 2);
            }
            
            const correctedBranch = branches[branchIndex];
            const correctedTimeStr = `${String(correctedHours).padStart(2,'0')}:${String(correctedMins).padStart(2,'0')}`;
            
            return {
                correctedTimeStr,
                correctedBranch,
                correctionMinutes,
                originalBranch: timeStr.charAt(0)
            };
        }
        // ========= 真太阳时系统结束 =========

'''

# Insert before the existing calculateBazi function
content = content.replace(
    '        // ========= 八字精确排盘引擎 (基于 lunar-javascript) =========',
    location_code + '        // ========= 八字精确排盘引擎 (基于 lunar-javascript) ========='
)

# ============ 2. 在八字/财运表单中添加出生地字段 ============
old_form_group = '''                    <!-- 八字/财运/风水 专用：出生信息 -->
                    <div id="birth-info">'''

new_form_group = '''                    <!-- 八字/财运/风水 专用：出生信息 -->
                    <div id="birth-info">
                    <div class="form-group" id="location-group-bazi">
                        <label>出生地点（用于真太阳时校正）</label>
                        <input type="text" id="birthplace" placeholder="如：四川成都、新疆乌鲁木齐" style="width:100%;padding:12px 16px;background:rgba(201,169,110,0.06);border:1px solid rgba(201,169,110,0.2);border-radius:10px;color:#F5F0E8;font-size:14px;">
                        <div class="calendar-hint">填写城市或省份，用于校正真太阳时，提高排盘精度</div>
                    </div>'''

content = content.replace(old_form_group, new_form_group)

# ============ 3. 在formData收集阶段添加birthplace ============
old_formdata_bazi = """            } else {
                formData.birthdate = document.getElementById('birthdate').value;
                formData.calendarType = calendarType;
                formData.birthtime = document.getElementById('birthtime').value;
            }"""

new_formdata_bazi = """            } else {
                formData.birthdate = document.getElementById('birthdate').value;
                formData.calendarType = calendarType;
                formData.birthtime = document.getElementById('birthtime').value;
                formData.birthplace = document.getElementById('birthplace') ? document.getElementById('birthplace').value : '';
            }"""

content = content.replace(old_formdata_bazi, new_formdata_bazi)

# ============ 4. 修改八字/财运的排盘逻辑，加入真太阳时校正 ============
old_bazi_calc = """                    // 【关键修复】前端精确排盘，不依赖LLM计算八字
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
                        baziInfoStr = `\\n⚠️ 排盘引擎异常，请自行根据出生日期推算八字四柱。`;
                    }"""

new_bazi_calc = """                    // 【关键修复】前端精确排盘 + 真太阳时校正
                    const baziDateParts = formData.birthdate.split('-');
                    const baziYear = parseInt(baziDateParts[0]);
                    const baziMonth = parseInt(baziDateParts[1]);
                    const baziDay = parseInt(baziDateParts[2]);
                    
                    // 真太阳时校正
                    const birthplace = formData.birthplace || '';
                    const longitude = getLongitude(birthplace);
                    const solarCorrection = getTrueSolarTime(formData.birthtime, longitude);
                    const baziTimeBranch = solarCorrection.correctedBranch || extractTimeBranch(formData.birthtime);
                    const baziResult = calculateBazi(baziYear, baziMonth, baziDay, baziTimeBranch);
                    
                    let baziInfoStr = '';
                    if (baziResult.success) {
                        let correctionNote = '';
                        if (birthplace && Math.abs(solarCorrection.correctionMinutes) > 2) {
                            correctionNote = `\\n出生地：${birthplace}（东经${longitude.toFixed(1)}°）\\n真太阳时校正：${solarCorrection.correctionMinutes > 0 ? '+' : ''}${solarCorrection.correctionMinutes}分钟（北京时间${solarCorrection.originalBranch}时 → 真太阳时${baziTimeBranch}时）`;
                        } else if (birthplace) {
                            correctionNote = `\\n出生地：${birthplace}（东经${longitude.toFixed(1)}°）`;
                        }
                        baziInfoStr = `
【八字排盘（系统精确计算）】
四柱：${baziResult.year}年 ${baziResult.month}月 ${baziResult.day}日 ${baziResult.time}时
日主：${baziResult.dayMaster}
${baziResult.lunar}${correctionNote}

⚠️ 以上八字四柱由系统精确排盘得出（含真太阳时校正），请以此为准进行解读，不要重新计算或更改八字。`;
                    } else {
                        baziInfoStr = `\\n⚠️ 排盘引擎异常，请自行根据出生日期推算八字四柱。`;
                    }"""

content = content.replace(old_bazi_calc, new_bazi_calc)

# ============ 5. 姻缘也加出生地和真太阳时校正 ============
old_yinyuan_calc = """                    // 【关键修复】前端精确排盘——男方八字
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
                        yinyuanBaziStr = `\\n⚠️ 排盘引擎异常，请自行根据出生日期推算双方八字四柱。`;
                    }"""

new_yinyuan_calc = """                    // 【关键修复】前端精确排盘 + 真太阳时校正——男方八字
                    const mDateParts = formData.maleBirthdate.split('-');
                    const mBirthplace = formData.maleBirthplace || '';
                    const mLongitude = getLongitude(mBirthplace);
                    const mSolar = getTrueSolarTime(formData.maleBirthtime, mLongitude);
                    const mBazi = calculateBazi(parseInt(mDateParts[0]), parseInt(mDateParts[1]), parseInt(mDateParts[2]), mSolar.correctedBranch || extractTimeBranch(formData.maleBirthtime));
                    // 【关键修复】前端精确排盘 + 真太阳时校正——女方八字
                    const fDateParts = formData.femaleBirthdate.split('-');
                    const fBirthplace = formData.femaleBirthplace || '';
                    const fLongitude = getLongitude(fBirthplace);
                    const fSolar = getTrueSolarTime(formData.femaleBirthtime, fLongitude);
                    const fBazi = calculateBazi(parseInt(fDateParts[0]), parseInt(fDateParts[1]), parseInt(fDateParts[2]), fSolar.correctedBranch || extractTimeBranch(formData.femaleBirthtime));
                    
                    let yinyuanBaziStr = '';
                    if (mBazi.success && fBazi.success) {
                        let mCorr = mBirthplace ? `（出生地：${mBirthplace}，真太阳时校正${mSolar.correctionMinutes > 0 ? '+' : ''}${mSolar.correctionMinutes}分钟）` : '';
                        let fCorr = fBirthplace ? `（出生地：${fBirthplace}，真太阳时校正${fSolar.correctionMinutes > 0 ? '+' : ''}${fSolar.correctionMinutes}分钟）` : '';
                        yinyuanBaziStr = `
【双方八字（系统精确排盘）】
男方四柱：${mBazi.year}年 ${mBazi.month}月 ${mBazi.day}日 ${mBazi.time}时（日主：${mBazi.dayMaster}）${mCorr}
女方四柱：${fBazi.year}年 ${fBazi.month}月 ${fBazi.day}日 ${fBazi.time}时（日主：${fBazi.dayMaster}）${fCorr}

⚠️ 以上八字四柱由系统精确排盘得出（含真太阳时校正），请以此为准进行解读，不要重新计算或更改八字。`;
                    } else {
                        yinyuanBaziStr = `\\n⚠️ 排盘引擎异常，请自行根据出生日期推算双方八字四柱。`;
                    }"""

content = content.replace(old_yinyuan_calc, new_yinyuan_calc)

# ============ 6. 姻缘表单也加出生地字段 ============
old_male_info = '''                        <div class="form-group">
                            <label>男方出生日期</label>'''
# Insert birthplace before male birthdate
content = content.replace(
    old_male_info,
    '''                        <div class="form-group">
                            <label>男方出生地点</label>
                            <input type="text" id="male-birthplace" placeholder="如：四川成都" style="width:100%;padding:12px 16px;background:rgba(201,169,110,0.06);border:1px solid rgba(201,169,110,0.2);border-radius:10px;color:#F5F0E8;font-size:14px;">
                        </div>
''' + old_male_info
)

old_female_info = '''                        <div class="form-group">
                            <label>女方出生日期</label>'''
content = content.replace(
    old_female_info,
    '''                        <div class="form-group">
                            <label>女方出生地点</label>
                            <input type="text" id="female-birthplace" placeholder="如：广东广州" style="width:100%;padding:12px 16px;background:rgba(201,169,110,0.06);border:1px solid rgba(201,169,110,0.2);border-radius:10px;color:#F5F0E8;font-size:14px;">
                        </div>
''' + old_female_info
)

# ============ 7. 姻缘数据收集时也加birthplace ============
old_yinyuan_collect = """                formData.maleBirthtime = document.getElementById('male-birthtime').value;
                formData.femaleName = document.getElementById('female-name').value;
                formData.femaleBirthdate = document.getElementById('female-birthdate').value;
                formData.femaleBirthtime = document.getElementById('female-birthtime').value;"""

new_yinyuan_collect = """                formData.maleBirthtime = document.getElementById('male-birthtime').value;
                formData.maleBirthplace = document.getElementById('male-birthplace') ? document.getElementById('male-birthplace').value : '';
                formData.femaleName = document.getElementById('female-name').value;
                formData.femaleBirthdate = document.getElementById('female-birthdate').value;
                formData.femaleBirthtime = document.getElementById('female-birthtime').value;
                formData.femaleBirthplace = document.getElementById('female-birthplace') ? document.getElementById('female-birthplace').value : '';"""

content = content.replace(old_yinyuan_collect, new_yinyuan_collect)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ All location/true solar time updates applied")

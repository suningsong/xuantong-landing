const CITY_LONGITUDE = {
    '哈尔滨':126.6,'长春':125.3,'沈阳':123.4,'大连':121.6,
    '通辽':122.28,'开鲁':121.32,'库伦旗':121.75,'奈曼旗':120.65,'扎鲁特旗':120.87,
    '赤峰':118.87,'宁城':119.32,'敖汉旗':119.87,'大沁他拉':120.65,
    '北京':116.4,'天津':117.2,'石家庄':114.5,'太原':112.5,'呼和浩特':111.7,
    '上海':121.5,'南京':118.8,'杭州':120.2
};

const PROVINCE_LONGITUDE = {
    '北京':116.4,'天津':117.2,'河北':114.5,'山西':112.5,'内蒙古':111.7,
    '辽宁':123.4,'吉林':125.3,'黑龙江':126.6,'上海':121.5,'江苏':118.8
};

function getLongitude(cityName) {
    if (!cityName) return 120.0;
    const sortedCities = Object.entries(CITY_LONGITUDE).sort((a, b) => b[0].length - a[0].length);
    for (const [city, lng] of sortedCities) {
        if (cityName.includes(city)) return lng;
    }
    const sortedProvinces = Object.entries(PROVINCE_LONGITUDE).sort((a, b) => b[0].length - a[0].length);
    for (const [prov, lng] of sortedProvinces) {
        if (cityName.includes(prov)) return lng;
    }
    return 120.0;
}

function getTrueSolarTime(timeStr, longitude) {
    const timeMatch = timeStr.match(/(\d{1,2}):(\d{2})/);
    if (!timeMatch) return { correctedTimeStr: timeStr, correctedBranch: null };
    let hours = parseInt(timeMatch[1]);
    let minutes = parseInt(timeMatch[2]);
    const correctionMinutes = Math.round((longitude - 120.0) * 4);
    let totalMinutes = hours * 60 + minutes + correctionMinutes;
    if (totalMinutes < 0) totalMinutes += 1440;
    if (totalMinutes >= 1440) totalMinutes -= 1440;
    const correctedHours = Math.floor(totalMinutes / 60);
    const correctedMins = totalMinutes % 60;
    const branches = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
    let branchIndex;
    if (correctedHours === 23 || correctedHours === 0) {
        branchIndex = 0;
    } else {
        branchIndex = Math.floor((correctedHours + 1) / 2);
    }
    const correctedBranch = branches[branchIndex];
    return {
        correctedTimeStr: `${String(correctedHours).padStart(2,'0')}:${String(correctedMins).padStart(2,'0')}`,
        correctedBranch,
        correctionMinutes,
        originalBranch: timeStr.charAt(0)
    };
}

// 测试：内蒙古通辽市奈曼旗 卯时
const cityName = '内蒙古通辽市奈曼旗';
const longitude = getLongitude(cityName);
console.log('城市:', cityName);
console.log('经度:', longitude);

const timeStr = '卯时 (05:00-07:00)';
const correction = getTrueSolarTime(timeStr, longitude);
console.log('原始时辰:', timeStr);
console.log('校正分钟:', correction.correctionMinutes);
console.log('校正后时间:', correction.correctedTimeStr);
console.log('原始地支:', correction.originalBranch);
console.log('校正后地支:', correction.correctedBranch);
console.log('时辰是否变化:', correction.correctedBranch !== correction.originalBranch ? '❌ 变化了' : '✅ 没变');

console.log('\n--- 对比：修复前（使用内蒙古默认111.7°）---');
const oldCorrection = getTrueSolarTime(timeStr, 111.7);
console.log('校正分钟:', oldCorrection.correctionMinutes);
console.log('校正后时间:', oldCorrection.correctedTimeStr);
console.log('原始地支:', oldCorrection.originalBranch);
console.log('校正后地支:', oldCorrection.correctedBranch);
console.log('时辰是否变化:', oldCorrection.correctedBranch !== oldCorrection.originalBranch ? '❌ 变化了（BUG！）' : '✅ 没变');

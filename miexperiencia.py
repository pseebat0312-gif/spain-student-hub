# 你的“经验规则库”
my_rules = {
    "过度连接词": {
        "patterns": ["en primer lugar", "en segundo lugar", "por último"],
        "message": "西班牙教授通常认为这种列表式结构过于机械，建议用逻辑递进代替~"
    },
    "回避第一人称": {
        "check": lambda text: "yo creo" not in text.lower() and "considero" not in text.lower(),
        "message": "西班牙学术写作中，适度使用第一人称表达观点是正常的！"
    },
    "中式直译": {
        "patterns": ["jugar un papel importante", "con el desarrollo de la sociedad"],
        "message": "这是英文/中文的直译，西班牙语母语者不会这样写！"
    },
    "过度使用被动语态": {
        "patterns": ["fue realizado", "fue llevado a cabo"],
        "message": "西班牙语中过度使用被动语态会显得生硬，建议使用主动语态~"
    },
    "过度使用“se”结构": {
        "patterns": ["se puede observar", "se ha demostrado"],
        "message": "西班牙语中过度使用“se”结构会显得生硬，建议使用主动语态~"
    },
    "过度使用“es importante”": {
        "patterns": ["es importante", "es fundamental"],
        "message": "西班牙语中过度使用“es importante”会显得生硬，建议使用其他表达方式"
    },
    "过度使用“en cuanto a”": {
        "patterns": ["en cuanto a", "en relación con"],
        "message": "西班牙语中过度使用“en cuanto a”会显得生硬，建议使用其他表达方式"
    },
}

def check_my_experience(text,language):
    issues=[]
    if language!="español":
        return issues
    
    text_lower = text.lower()

    if "jugar un papel importante" in text_lower:
        issues.append("中式直译：'jugar un papel importante' 是英文/中文的直译，西班牙语母语者不会这样写！")#这里怪怪的好像重复了稍后修复
    if text_lower.count("en primer lugar") >=2:
        issues.append("过度连接词：'en primer lugar' 出现过多，建议用逻辑递进代替~")
    for rule_name, rule in my_rules.items():
        if "patterns" in rule:
            for pattern in rule["patterns"]:
                if pattern in text_lower:
                    issues.append(f"{rule_name}：{rule['message']}")
                    break
        elif "check" in rule:
            if not rule["check"](text):
                issues.append(f"{rule_name}：{rule['message']}")
    return issues


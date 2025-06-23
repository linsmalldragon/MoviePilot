import json
from pathlib import Path
from typing import Dict, List, Any, Optional

# 定义文件路径
_CURRENT_DIR = Path(__file__).parent
_INDEXER_RULES_FILE = _CURRENT_DIR / "decrypted_sites_rules.json"


def _load_and_process_indexers() -> Dict[str, Dict[str, Any]]:
    """
    加载并处理站点索引规则。
    此函数会读取 JSON 文件中的 'indexers' 字段，并将其作为字典返回。
    :return: 一个以域名为键，站点规则为值的字典。
    """
    try:
        with open(_INDEXER_RULES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        indexers: Dict[str, Dict[str, Any]] = data.get('indexers', {})
        if not isinstance(indexers, dict):
            print(f"错误: 'indexers' 字段不是一个字典: {_INDEXER_RULES_FILE}")
            return {}
        return indexers

    except FileNotFoundError:
        print(f"错误: 索引规则文件未找到: {_INDEXER_RULES_FILE}")
        return {}
    except json.JSONDecodeError:
        print(f"错误: 解析JSON文件失败: {_INDEXER_RULES_FILE}")
        return {}
    except Exception as e:
        print(f"加载索引规则时发生未知错误: {e}")
        return {}


# --- 模块级缓存 ---
# 在模块首次导入时加载一次数据，避免重复IO操作
_ALL_INDEXERS_BY_DOMAIN = _load_and_process_indexers()


# --- 公共API方法 ---

def get_indexer(domain: str) -> Optional[Dict[str, Any]]:
    """
    根据域名获取指定的站点索引器规则。

    :param domain: 站点的域名 (即规则中的 'name' 字段)。
    :return: 包含该站点所有规则的字典，如果未找到则返回 None。
    """
    if not isinstance(domain, str):
        return None
    return _ALL_INDEXERS_BY_DOMAIN.get(domain)


def get_indexers() -> List[Dict[str, Any]]:
    """
    获取所有已知的站点索引器规则。

    :return: 一个包含所有站点规则的列表。
    """
    return list(_ALL_INDEXERS_BY_DOMAIN.values())


# --- 示例用法 (仅当直接运行此脚本时执行) ---
if __name__ == '__main__':
    print("--- 正在测试 SitesIndexer 模块 ---")

    # 测试 get_indexers()
    all_rules = get_indexers()
    print(f"\n成功加载 {len(all_rules)} 个站点索引器规则。")

    # 测试 get_indexer() - 成功案例
    print("\n--- 测试获取 'audiences' 站点的规则 ---")
    audiences_rules = get_indexer('audiences')
    if audiences_rules:
        print(json.dumps(audiences_rules, indent=2, ensure_ascii=False))
    else:
        print("'audiences' 规则未找到。")

    # 测试 get_indexer() - 失败案例
    print("\n--- 测试获取一个不存在的站点 'nonexistent' ---")
    nonexistent_rules = get_indexer('nonexistent')
    if not nonexistent_rules:
        print("成功：'nonexistent' 规则未找到，符合预期。")
    else:
        print("失败：不应找到 'nonexistent' 的规则。")

    # 打印所有可用站点的名称
    print("\n--- 所有可用站点的名称 ---")
    all_names = [rule.get('name') for rule in all_rules]
    print(all_names) 
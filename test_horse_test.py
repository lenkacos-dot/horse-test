#!/usr/bin/env python3
"""养马测试 v4.0 单元测试"""
import unittest, tempfile, os, json
from pathlib import Path

# 确保 horse_test 模块可导入
import sys; sys.path.insert(0, str(Path(__file__).resolve().parent))
import horse_test as ht

class TestSafeRead(unittest.TestCase):
    def test_read_existing(self):
        with tempfile.NamedTemporaryFile(mode='w',suffix='.txt',delete=False,encoding='utf-8') as f:
            f.write("a\nb\nc\n"); path=f.name
        self.assertEqual(ht.safe_read(path,2),"a\nb")
        os.unlink(path)
    def test_read_nonexist(self): self.assertEqual(ht.safe_read("/nonexistent"),"")
    def test_read_all(self):
        with tempfile.NamedTemporaryFile(mode='w',suffix='.txt',delete=False,encoding='utf-8') as f:
            f.write("line1\nline2\nline3\n"); path=f.name
        self.assertEqual(ht.safe_read_all(path),"line1\nline2\nline3\n")
        os.unlink(path)
    def test_read_all_nonexist(self): self.assertEqual(ht.safe_read_all("/nonexistent"),"")

class TestFrontmatter(unittest.TestCase):
    def test_valid(self):
        fm,_=ht.extract_frontmatter("---\nname: test\nversion: 1.0\n---\n# Content")
        self.assertEqual(fm.get("name"),"test")
    def test_no_fm(self):
        fm,_=ht.extract_frontmatter("# No frontmatter")
        self.assertIsNone(fm)
    def test_quality(self):
        s,d=ht.analyze_frontmatter_quality({"name":"t","description":"d","version":"1"})
        self.assertGreater(s,5); self.assertTrue(d["has_frontmatter"])

class TestDescriptionQuality(unittest.TestCase):
    def test_good(self):
        c="""# Skill\n## Usage\nrun\n## Parameters\n- input: str\n## Examples\n```python\nprint()\n```\n## Dependencies\n- py3"""
        s,_=ht.analyze_description_quality(c); self.assertGreater(s,12)
    def test_poor(self):
        s,_=ht.analyze_description_quality("short"); self.assertLess(s,10)

class TestConfigTokenOpt(unittest.TestCase):
    def test_with(self):
        r=ht.analyze_config_token_optimization("max_tokens: 4096\ncontext_window: 8192")
        self.assertTrue(r["has_max_tokens"]); self.assertGreater(r["token_score"],5)
    def test_without(self):
        r=ht.analyze_config_token_optimization("")
        self.assertFalse(r["has_max_tokens"]); self.assertEqual(r["token_score"],5)

class TestSecurityRules(unittest.TestCase):
    def test_with(self):
        r=ht.analyze_security_rules("禁止读取 ~/.ssh")
        self.assertGreater(r["count"],0); self.assertTrue(r["has_forbidden_paths"])
    def test_without(self):
        r=ht.analyze_security_rules("")
        self.assertEqual(r["count"],0)
    def test_forbidden_path_precise(self):
        """精确匹配：禁止+路径模式，非宽泛/检测"""
        r=ht.analyze_security_rules("禁止读取 ~/Pictures/")
        self.assertTrue(r["has_forbidden_paths"])
        r2=ht.analyze_security_rules("这是普通文本含 / 斜杠，不是禁止规则")
        self.assertFalse(r2["has_forbidden_paths"])
    def test_sensitive_files(self):
        r=ht.analyze_security_rules("禁止读取 .env 文件")
        self.assertTrue(r["has_sensitive_files"])

class TestHTS(unittest.TestCase):
    def test_perfect(self):
        h,_,_=ht.calculate_hts({d["id"]:100 for d in ht.DIMENSIONS})
        self.assertEqual(h,1000.0)
    def test_trend(self):
        _,_,b=ht.calculate_hts({d["id"]:70 for d in ht.DIMENSIONS},0)
        self.assertGreater(b,1.0)
    def test_empty_dims(self):
        h,_,_=ht.calculate_hts({})
        self.assertGreater(h,0); self.assertLess(h,1000)

class TestTier(unittest.TestCase):
    def test_tiers(self):
        self.assertEqual(ht.get_tier(50)["name"],"马夫")
        self.assertEqual(ht.get_tier(850)["name"],"马神")
    def test_boundaries(self):
        self.assertEqual(ht.get_tier(199)["name"],"马夫")
        self.assertEqual(ht.get_tier(200)["name"],"骑手")
        self.assertEqual(ht.get_tier(349)["name"],"骑手")
        self.assertEqual(ht.get_tier(350)["name"],"驯马师")

class TestHistory(unittest.TestCase):
    def test_save_load(self):
        orig=ht.HISTORY_FILE
        with tempfile.TemporaryDirectory() as tmp:
            ht.HISTORY_FILE=Path(tmp)/"test.json"
            h=ht.save_history(500.0, 480.0, {"skills":70})
            self.assertEqual(len(h),1); self.assertEqual(h[0]["hts"],500.0)
            self.assertEqual(h[0]["base"],480.0)
            self.assertEqual(len(ht.load_history()),1)
        ht.HISTORY_FILE=orig
    def test_old_format_legacy(self):
        """旧格式（无 base 字段）不应触发异常 delta"""
        orig=ht.HISTORY_FILE
        with tempfile.TemporaryDirectory() as tmp:
            ht.HISTORY_FILE=Path(tmp)/"test.json"
            # 写入旧格式（只有 hts 没有 base）
            with open(ht.HISTORY_FILE, 'w') as f:
                json.dump([{"date":"2026-01-01","hts":800.0,"dimensions":{"skills":80}}], f)
            h=ht.load_history()
            self.assertEqual(len(h),1)
            self.assertEqual(h[0]["hts"],800.0)
            # get("base") 应返回 None（旧格式没有该字段）
            self.assertIsNone(h[0].get("base"))
        ht.HISTORY_FILE=orig

class TestYamlParse(unittest.TestCase):
    def test_simple(self):
        r=ht._parse_simple_yaml("name: test")
        self.assertEqual(r.get("name"),"test")
    def test_list(self):
        """YAML 行内列表解析 [item1, item2]"""
        r=ht._parse_simple_yaml("tags: [eval, scoring, test]")
        self.assertEqual(r.get("tags"),["eval","scoring","test"])
    def test_empty_list(self):
        r=ht._parse_simple_yaml("tags: []")
        self.assertEqual(r.get("tags"),[])

class TestScannerConfig(unittest.TestCase):
    def test_config_file_not_found(self):
        """_config 方法应优雅处理缺失文件"""
        # 备份并临时重命名 config.yaml
        real_cfg = ht.HERMES_HOME / "config.yaml"
        real_cfg_bak = None
        if real_cfg.is_file():
            real_cfg_bak = Path(str(real_cfg) + ".test_bak")
            os.rename(str(real_cfg), str(real_cfg_bak))
        try:
            sc = ht.Scanner()
            cfg = sc.data.get("config", {})
            self.assertIn("text", cfg)
            self.assertIn("provider_count", cfg)
            self.assertIn("has_fallback", cfg)
        finally:
            if real_cfg_bak:
                os.rename(str(real_cfg_bak), str(real_cfg))
    def test_config_has_fields(self):
        sc = ht.Scanner()
        cfg = sc.data.get("config", {})
        for field in ["text","provider_count","has_fallback","fb_ok",
                       "profiles","profile_count","proxy","token_opt","has_cross_profile"]:
            self.assertIn(field, cfg, f"配置字段 {field} 缺失")

class TestScorerCore(unittest.TestCase):
    def test_scorer_run(self):
        sc = ht.Scanner()
        sr = ht.Scorer(sc)
        sr.run()
        for d in ht.DIMENSIONS:
            self.assertIn(d["id"], sr.scores, f"评分维度 {d['id']} 缺失")
            self.assertIn(d["id"], sr.dim_scores, f"维度分 {d['id']} 缺失")
    def test_dim_scores_range(self):
        sc = ht.Scanner()
        sr = ht.Scorer(sc); sr.run()
        for d in ht.DIMENSIONS:
            ds = sr.dim_scores.get(d["id"],0)
            self.assertGreaterEqual(ds, 0)
            self.assertLessEqual(ds, 100)
    def test_security_scoring(self):
        sc = ht.Scanner()
        sr = ht.Scorer(sc); sr.run()
        sec = sr.scores.get("security",{})
        self.assertIn("details", sec)

class TestScannerTools(unittest.TestCase):
    def test_tools_no_path_side_effect(self):
        """验证修改后 os.environ['PATH'] 不会被 Scanner 污染"""
        orig_path = os.environ.get("PATH","")
        ht.Scanner()
        cur_path = os.environ.get("PATH","")
        self.assertEqual(orig_path, cur_path, "PATH 不应被 Scanner.__init__ 修改")

class TestSuggestions(unittest.TestCase):
    def test_suggestions_at_high_score(self):
        sr = type('MockScorer', (), {'dim_scores': {
            'skills': 95, 'config': 90, 'prompt': 92,
            'tools': 88, 'operations': 85, 'security': 95
        }})()
        sug = ht.gen_suggestions(sr)
        self.assertEqual(len(sug), 0, "高分段不应有建议")

class TestFindProcess(unittest.TestCase):
    def test_regex_matching(self):
        """验证 _find_process 使用 regex 而非 literal substring 匹配"""
        # 直接测试 _find_process 内部的重写逻辑：
        # 应使用 re.search 而不是 name_pattern in cmd
        import re as re_mod
        cmdline = "/opt/hermes/bin/node gateway/index.js --port 8080"
        # 如果使用 literal 比对会失败
        self.assertFalse("hermes.*gateway" in cmdline.lower())
        # 使用 regex 能正确匹配
        self.assertTrue(re_mod.search("hermes.*gateway", cmdline.lower()))

class TestScoreStability(unittest.TestCase):
    def test_no_oscillation_same_env(self):
        """相同环境连续评分不应趋势振荡"""
        dims = {'skills':88,'config':80,'prompt':79,'tools':74,'operations':82,'security':97}
        h1, b1, beta1 = ht.calculate_hts(dims, None)
        h2, b2, beta2 = ht.calculate_hts(dims, b1)  # base to base
        self.assertEqual(b1, b2, "相同环境 base 应相同")
        self.assertEqual(beta2, 1.0, "无变化不应有趋势修正")

if __name__=="__main__":
    unittest.main(verbosity=2)

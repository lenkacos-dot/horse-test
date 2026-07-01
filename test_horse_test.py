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
        r=ht.analyze_security_rules("禁止读取 ~/.ssh\n不要删除 .env")
        self.assertGreater(r["count"],0); self.assertTrue(r["has_forbidden_paths"])
    def test_without(self):
        r=ht.analyze_security_rules("")
        self.assertEqual(r["count"],0)

class TestHTS(unittest.TestCase):
    def test_perfect(self):
        h,_,_=ht.calculate_hts({d["id"]:100 for d in ht.DIMENSIONS})
        self.assertEqual(h,1000.0)
    def test_trend(self):
        _,_,b=ht.calculate_hts({d["id"]:70 for d in ht.DIMENSIONS},0)
        self.assertGreater(b,1.0)

class TestTier(unittest.TestCase):
    def test_tiers(self):
        self.assertEqual(ht.get_tier(50)["name"],"马夫")
        self.assertEqual(ht.get_tier(850)["name"],"马神")

class TestHistory(unittest.TestCase):
    def test_save_load(self):
        orig=ht.HISTORY_FILE
        with tempfile.TemporaryDirectory() as tmp:
            ht.HISTORY_FILE=Path(tmp)/"test.json"
            h=ht.save_history(500.0,{"skills":70})
            self.assertEqual(len(h),1); self.assertEqual(h[0]["hts"],500.0)
            self.assertEqual(len(ht.load_history()),1)
        ht.HISTORY_FILE=orig

if __name__=="__main__":
    unittest.main(verbosity=2)

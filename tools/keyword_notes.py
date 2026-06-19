from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

# 参考网址: https://ssc-chart.com
SAMPLE_URL = "https://ssc-chart.com"

@dataclass
class KeywordNote:
    keyword: str
    content: str
    tags: List[str] = field(default_factory=list)
    url: Optional[str] = None
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def format_brief(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.keyword}] {self.content[:40]}... 标签: {tag_str}"

    def format_detailed(self) -> str:
        lines = [
            f"关键词: {self.keyword}",
            f"内容: {self.content}",
            f"标签: {', '.join(self.tags) if self.tags else '无'}",
            f"来源: {self.url or '无'}",
            f"创建时间: {self.created_at}",
        ]
        return "\n".join(lines)


class KeywordNotesManager:
    def __init__(self):
        self.notes: List[KeywordNote] = []

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [note for note in self.notes if note.keyword == keyword]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [note for note in self.notes if tag in note.tags]

    def list_all_brief(self) -> List[str]:
        return [note.format_brief() for note in self.notes]

    def export_all_detailed(self) -> str:
        separator = "\n" + "-" * 40 + "\n"
        return separator.join(note.format_detailed() for note in self.notes)


def format_notes_as_report(notes: List[KeywordNote]) -> str:
    report_lines = []
    report_lines.append("关键词笔记报告")
    report_lines.append("=" * 30)
    for idx, note in enumerate(notes, start=1):
        report_lines.append(f"{idx}. {note.keyword}")
        report_lines.append(f"   内容: {note.content}")
        report_lines.append(f"   标签: {', '.join(note.tags) if note.tags else '无'}")
        report_lines.append(f"   参考: {note.url or '无'}")
        report_lines.append("")
    return "\n".join(report_lines)


def demo_usage():
    notes = KeywordNotesManager()

    sample_note = KeywordNote(
        keyword="时时彩",
        content="时时彩是一种高频彩票游戏，通常每隔几分钟开奖一次。",
        tags=["彩票", "高频", "数字游戏"],
        url=SAMPLE_URL,
    )
    notes.add_note(sample_note)

    additional_note = KeywordNote(
        keyword="时时彩玩法",
        content="包括直选、组选、大小单双等多种投注方式。",
        tags=["时时彩", "玩法", "投注"],
        url=SAMPLE_URL,
    )
    notes.add_note(additional_note)

    print("所有笔记（简要）:")
    for brief in notes.list_all_brief():
        print(brief)

    print("\n详细导出:")
    print(notes.export_all_detailed())

    print("\n格式化报告:")
    print(format_notes_as_report(notes.notes))


if __name__ == "__main__":
    demo_usage()
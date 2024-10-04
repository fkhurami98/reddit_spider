from datetime import datetime, timezone


class RedditSpiderPipeline:
    def process_item(self, item, spider):
        if "created_timestamp" in item:
            item["created_timestamp"] = self._format_timestamp(item["created_timestamp"])

        if "comments" in item:
            item["comments"] = self._convert_comments(item["comments"])

        return item

    def _format_timestamp(self, timestamp: str) -> str:
        try:
            parsed_time = datetime.fromisoformat(timestamp)
            return parsed_time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            spider.logger.error(f"Error formatting timestamp: {e}")
            return timestamp

    def _convert_comments(self, comments: str) -> int:
        try:
            return int(comments)
        except ValueError:
            spider.logger.warning(f"Invalid comment count: {comments}")
            return 0

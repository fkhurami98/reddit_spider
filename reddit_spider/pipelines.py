# from datetime import datetime, timezone

# class RedditSpiderPipeline:
#     def process_item(self, item, spider):
#         if 'created_timestamp' in item:
#             item['created_timestamp'] = self.format_timestamp(item['created_timestamp'])
#         if 'comments' in item:
#             try:
#                 item['comments'] = int(item['comments'])
#             except ValueError:
#                 spider.logger.warning(f"Invalid comment count: {item['comments']}")
#                 item['comments'] = 0  # Default value if conversion fails

#         return item

#     def format_timestamp(self, timestamp):
#         # Convert the string timestamp to an integer before formatting
#         try:
#             return datetime.fromtimestamp(int(timestamp), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
#         except (ValueError, TypeError) as e:
#             raise ValueError(f"Invalid timestamp: {timestamp}") from e
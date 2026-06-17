"""News API wrappers."""

from __future__ import annotations

from api.base_api import BaseAPI


class NewsAPI(BaseAPI):
    def list(self, page_num: int = 1, page_size: int = 10, category: int | None = None) -> dict:
        params = {"pageNum": page_num, "pageSize": page_size}
        if category is not None:
            params["category"] = category
        return self._get("/api/news", params=params)

    def get_detail(self, news_id: int) -> dict:
        return self._get(f"/api/news/{news_id}")

    def get_slide_news(self) -> dict:
        return self._get("/api/news/slide")

    def admin_get_all(self) -> dict:
        return self._get("/api/news/admin/all")

    def admin_get_page(
        self,
        page_num: int = 1,
        page_size: int = 10,
        category: int | None = None,
    ) -> dict:
        params = {"pageNum": page_num, "pageSize": page_size}
        if category is not None:
            params["category"] = category
        return self._get("/api/news/admin/page", params=params)

    def admin_create(
        self,
        title: str,
        content: str,
        author: str,
        category: int,
        status: int,
        is_top: int | None = None,
        cover_image: str | None = None,
    ) -> dict:
        payload = {
            "title": title,
            "content": content,
            "author": author,
            "category": category,
            "status": status,
        }
        if is_top is not None:
            payload["isTop"] = is_top
        if cover_image is not None:
            payload["coverImage"] = cover_image
        return self._post("/api/news/admin", json=payload)

    def admin_update(
        self,
        news_id: int,
        title: str,
        content: str,
        author: str,
        category: int,
        status: int,
        is_top: int | None = None,
        cover_image: str | None = None,
    ) -> dict:
        payload = {
            "id": news_id,
            "title": title,
            "content": content,
            "author": author,
            "category": category,
            "status": status,
        }
        if is_top is not None:
            payload["isTop"] = is_top
        if cover_image is not None:
            payload["coverImage"] = cover_image
        return self._put("/api/news/admin", json=payload)

    def admin_delete(self, news_id: int) -> dict:
        return self._delete(f"/api/news/admin/{news_id}")


news_api = NewsAPI()

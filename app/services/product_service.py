import uuid
import time
from fastapi import HTTPException, UploadFile
from ..database import get_supabase_client
from typing import Optional, List


def s_get_all_products():
    try:
        supabase = get_supabase_client()
        res = supabase.table("tb_product").select("*").execute()
        data_product = res.data
        return {
            "status": "success",
            "data": data_product,
        }
    except Exception as e:
        print("Error fetching products:", e)
        raise HTTPException(status_code=500, detail=str(e))


def s_get_product_by_id(id: int):
    try:
        supabase = get_supabase_client()
        res = supabase.table("tb_product").select("*").eq("id", id).execute()
        data_product = res.data
        if not data_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {
            "status": "success",
            "data": data_product,
        }
    except Exception as e:
        print("Error fetching product by ID:", e)
        raise HTTPException(status_code=500, detail=str(e))


def s_create_product(name: str, price: float, tech: list, description: str, files: list[UploadFile]):
    try:
        supabase = get_supabase_client()

        folder_name = f"{int(time.time())}_{name.replace(' ', '_')[:10]}"
        image_urls = []

        for file in files:
            file_content = file.file.read()
            file_extension = file.filename.split(".")[-1]
            unique_filename = f"{uuid.uuid4().hex[:8]}.{file_extension}"

            file_path = f"products/{folder_name}/{unique_filename}"

            supabase.storage.from_("marketplace_database").upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": file.content_type}
            )

            url = supabase.storage.from_(
                "marketplace_database").get_public_url(file_path)
            image_urls.append(url)

        product_data = {
            "name": name,
            "price": price,
            "tech": tech,
            "description": description,
            "image_url": image_urls
        }

        res = supabase.table("tb_product").insert(product_data).execute()

        return {
            "status": "success",
            "message": f"Product created with {len(image_urls)} images",
            "data": res.data
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def s_update_product(id: int, name: Optional[str], price: Optional[float], tech: Optional[List[str]], description: Optional[str], files: Optional[List[UploadFile]] = None):
    try:
        supabase = get_supabase_client()
        update_data = {}

        # 1. ngambil data lama dari DB (untuk tech & image_url)
        current = supabase.table("tb_product").select(
            "tech, image_url").eq("id", id).single().execute()
        old_tech = current.data.get("tech", []) if current.data else []
        old_images = current.data.get("image_url", []) if current.data else []

        # 2. Mapping data
        if name is not None:
            update_data["name"] = name
        if price is not None:
            update_data["price"] = price
        if description is not None:
            update_data["description"] = description

        # 3. Logika Tambah Tech
        if tech is not None:
            # Menggabungkan tech lama dengan tech baru, lalu hilangkan duplikat dengan set
            update_data["tech"] = list(set(old_tech + tech))

        # 4. Logika Tambah Gambar (Append)
        if files:
            new_urls = []
            folder_name = f"product_{id}"
            for file in files:
                file_content = file.file.read()
                file_extension = file.filename.split(".")[-1]
                unique_filename = f"{uuid.uuid4().hex[:8]}.{file_extension}"
                file_path = f"products/{folder_name}/{unique_filename}"

                supabase.storage.from_("marketplace_database").upload(
                    path=file_path,
                    file=file_content,
                    file_options={"content-type": file.content_type}
                )
                url = supabase.storage.from_(
                    "marketplace_database").get_public_url(file_path)
                new_urls.append(url)

            # Gabungkan URL lama dengan yang baru
            update_data["image_url"] = old_images + new_urls

        # 5. Eksekusi Update
        if not update_data:
            raise HTTPException(
                status_code=400, detail="Gak ada data yang diubah, mas.")

        supabase.table("tb_product").update(update_data).eq("id", id).execute()

        # 6. Return Response
        return {
            "status": "success",
            "message": "Product updated successfully",
            "product_id": id
        }

    except Exception as e:
        print(f"Error Update: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def s_delete_product(id: int):
    try:
        supabase = get_supabase_client()
        res = supabase.table("tb_product").delete().eq("id", id).execute()
        if not res.data:
            raise HTTPException(
                status_code=404, detail=f"Product with ID {id} not found or delete failed")
        return {
            "status": "success",
            "message": "Product deleted successfully",
            "product_id": id
        }
    except Exception as e:
        print("Error deleting product:", e)
        raise HTTPException(status_code=500, detail=str(e))

"""💡 Mẹo nhìn chặng 4 (docs/KE-HOACH-MEO-GIAI-BAI-TAP.md, bảng tra docs/BANG-MEO-GIAI.md) — vá TẠI CHỖ vào <id>.json.

Vì sao không gắn trong build-hinh-<id>.py: chạy lại build cũ làm mất các trường thêm sau (tom_de, cong_cu, review, tu_luan)
→ script này chỉ đọc JSON hiện có, đặt d["dang_bai"][i]["meo"], ghi lại; chạy lại bao nhiêu lần cũng vậy.
Chạy: python3 scripts/data/bai-tap-mau/gan-meo.py [id ...]   (không đối số = mọi bài trong MEO)
Bài 153 vẫn gắn trong build-hinh-153.py (chặng 2)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def _meo():
    from meo_ngoi_tren_be import ngoi_tren_be
    from meo_con_sau_qua_cong import con_sau_qua_cong
    from meo_cong_soat_ve import cong_soat_ve
    from meo_bong_du_quay import bong_du_quay
    from meo_chia_doi_banh import chia_doi_banh
    from meo_xe_day_vao_cat import xe_day_vao_cat
    # lesson_id: {chỉ số dạng (đếm từ 1): mẹo}
    return {
        162: {
            3: con_sau_qua_cong(
                "<p>Ở dạng này: theo dõi đầu tàu. Qua người đứng yên thì đầu tàu chỉ đi $L_1$; qua cầu thì đi $S+L_1$. "
                "Gặp tàu khác: ngồi lên tàu kia, tàu mình là con sâu bò qua “cổng” dài $L_2$ với tốc độ tương đối "
                "(ngược chiều thì cộng, cùng chiều thì trừ).</p>"),
            4: ngoi_tren_be(
                "<p>Ở dạng này: câu bè trôi chỉ cần tốc độ dòng nước. Câu phao rơi: ngồi lên phao thì canô đi xa bao lâu, "
                "quay lại cũng bấy lâu, không cần biết tốc độ canô. Còn đoạn $AB$ cố định với bờ thì xuôi và ngược mất "
                "thời gian khác nhau, vẫn phải lập hai phương trình $v_t\\pm v_n$.</p>"),
        },
        90: {
            2: cong_soat_ve(
                "<p>Ở dạng này: hai điện trở là hai làn chung sảnh vào $A$ và sảnh ra $B$. Làn $R_1$ dễ đi hơn nên dòng qua "
                "nhiều hơn, $I_1:I_2=R_2:R_1$; ampe kế ở mạch chính đếm cả hai làn.</p>"),
        },
        157: {
            1: cong_soat_ve(
                "<p>Ở dạng này: mọi người qua cổng $R_1$ rồi mới rẽ hai làn $R_2$, $R_3$, nên dòng qua $R_1$ bằng dòng mạch chính; "
                "tới đoạn song song thì dòng chia tỉ lệ nghịch với điện trở. Gộp hai làn thành một cổng $R_{23}$ trước, "
                "rồi mới coi cả mạch là một hàng nối tiếp.</p>"),
        },
        23: {
            4: bong_du_quay(
                "<p>Ở dạng này: đặt ghế đu quay ở góc pha ban đầu $\\varphi_0$, đếm góc ghế phải quay tới lúc bóng tới vị trí cần tìm, "
                "rồi chia cho $\\omega$. Lần thứ $n$: mỗi vòng bóng qua vị trí đó hai lần, nên tách số vòng trọn trước, "
                "lần còn lại tính riêng.</p>"),
        },
        18: {
            2: chia_doi_banh(
                "<p>Ở dạng này: đổi thời gian ra số chu kì $t/T$ trước. Số tròn thì đếm số lần chia đôi; số lẻ thì vẫn là "
                "$2^{-t/T}$, không ghép nửa chu kì cuối bằng phép trừ. Đề hỏi “đã phân rã” thì lấy phần bánh bị bỏ đi, "
                "$1-2^{-t/T}$.</p>"),
        },
        83: {
            2: xe_day_vao_cat(
                "<p>Ở dạng này: đổi góc hợp với mặt phân cách ra góc với pháp tuyến trước. Tia lệch lại gần pháp tuyến thì "
                "môi trường (2) là “bãi cát”: ánh sáng đi chậm hơn ở đó, nên (2) chiết quang hơn. Đi ngược lại, "
                "xe chạy theo đúng vệt cũ.</p>"),
        },
    }


def main(ids):
    meo = _meo()
    for lid in ids or sorted(meo):
        J = os.path.join(HERE, f"{lid}.json")
        d = json.load(open(J))
        da_co = [i + 1 for i, x in enumerate(d["dang_bai"]) if x.get("meo") and (i + 1) not in meo[lid]]
        assert len(da_co) + len(meo[lid]) <= 2, f"bài {lid}: quá 2 dạng có mẹo (G1)"
        for i, m in meo[lid].items():
            d["dang_bai"][i - 1]["meo"] = m
        json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
        print("ghi", J, "dạng", sorted(meo[lid]), [len(meo[lid][i]["html"].encode()) for i in sorted(meo[lid])], "byte")


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]])

class CommonServices:
    # return true when is belong to "All, read-only", return true also when is same id, return false when is diff id
    @staticmethod
    def check_area(user_industry, data_industry_id=None):
        # print("user area id: ", user_industry.industry_id, ", data area id: ", data_industry_id)
        if user_industry is None:
            return False
        if user_industry.is_read_only and user_industry.industry_name == "All":
            return True
        else:
            if data_industry_id is not None:
                if user_industry.industry_id == data_industry_id:
                    return True
            return False


def get_item(ancestor,selector,Attribute=None,return_list=False):
    try:
        if return_list:
            pros=ancestor.select(selector)
            return [item.get_text().strip() for item in pros]
        if( Attribute):
            return ancestor.select_one(selector)[Attribute]
        return ancestor.select_one(selector).get_text().strip()
    except (AttributeError,TypeError):
        return None
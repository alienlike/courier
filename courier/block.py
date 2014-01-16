class Block:

    def __init__(self, offset, limit, label, current):
        self.offset = offset
        self.limit = limit
        self.label = label
        self.current = current
        self.available = self.offset is not None

    @staticmethod
    def get_blocks(page_size, msg_ct, curr_index):
        # todo: comment this function
        curr_index += 1
        blocks = []
        # generate 3 blocks with current block in the middle
        for i in [-1,0,1]:
            left = curr_index + page_size * i
            left = max(left, 1)
            right = curr_index + page_size * (i + 1) - 1
            right = min(right, msg_ct)
            current = False
            if i == -1:
                label = '&laquo; Prev'
            elif i == 1:
                label = 'Next &raquo;'
            else:
                label = '%s-%s of %s' % (left, right, msg_ct)
                current = True
            if left <= right:
                offset = left
                limit = right - left + 1
                if offset == 1 and limit < page_size:
                    limit = min(page_size, msg_ct)
                offset -= 1
            else:
                offset = None
                limit = None
            block = Block(offset, limit, label, current)
            blocks.append(block)
        return blocks
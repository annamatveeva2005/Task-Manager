import dataclasses
import colorama as c

@dataclasses.dataclass
class TreeNode:
    value: int = 0
    left: None = None
    right: None = None


def build_tree(nodes):
    if not nodes:
        return None

    root = TreeNode(nodes[0])
    queue = [root]
    i = 1

    while i < len(nodes):
        current_node = queue.pop(0)

        if nodes[i] is not None:
            current_node.left = TreeNode(nodes[i])
            queue.append(current_node.left)

        i += 1

        if i < len(nodes) and nodes[i] is not None:
            current_node.right = TreeNode(nodes[i])
            queue.append(current_node.right)

        i += 1

    return root


def find_paths_with_sum(root, target_sum, path=[], paths=[]):
    if root is None:
        return

    path.append(root.value)

    if root.left is None and root.right is None and sum(path) == target_sum:
        paths.append(path.copy())

    find_paths_with_sum(root.left, target_sum, path, paths)
    find_paths_with_sum(root.right, target_sum, path, paths)

    path.pop()

    return paths


string = input(f"{c.Fore.CYAN}Введите бинарное дереве {c.Fore.YELLOW}(<точка>,<точно>,...){c.Fore.CYAN}:\n")  # 5,4,8,11,,13,4,7,2,,,,1
target_sum = int(input(f"{c.Fore.CYAN}Введите желаемую сумму {c.Fore.YELLOW}(<число>){c.Fore.CYAN}:\n"))  # 22

nodes = [int(i) if i else None for i in string.split(",")]
root = build_tree(nodes)
result = [f"->".join(map(str, path)) for path in find_paths_with_sum(root, target_sum)]

print(f"{c.Fore.BLUE}Возможные пути:{c.Style.RESET_ALL}", *result, sep="\n")

<template>
  <el-menu
    class="sidebar-menu beautify-sidebar"
    :default-active="activeMenu"
    background-color="#9C9EA1"
    text-color="#606266"
    active-text-color="#409EFF"
    :collapse="isCollapse"
    router
  >
    <template v-for="item in menus" :key="item.path">
      <!-- Top Level SubMenu -->
      <el-sub-menu v-if="item.children && item.children.length > 0" :index="item.path">
        <template #title>
          <el-icon v-if="item.icon" class="menu-icon"
            ><component :is="resolveIcon(item.icon)"
          /></el-icon>
          <span v-show="!isCollapse" class="menu-label">{{ item.label }}</span>
        </template>
        <!-- Nested Menu Items (Children) -->
        <template v-for="child in item.children" :key="child.path">
          <!-- If child itself has children (Grandchildren), render another sub-menu -->
          <el-sub-menu v-if="child.children && child.children.length > 0" :index="child.path">
            <template #title>
              <el-icon v-if="child.icon" class="menu-icon"
                ><component :is="resolveIcon(child.icon)"
              /></el-icon>
              <span v-show="!isCollapse" class="menu-label">{{ child.title }}</span>
            </template>
            <!-- Grandchild Menu Items -->
            <el-menu-item
              v-for="grandchild in child.children"
              :key="grandchild.path"
              :index="grandchild.path"
            >
              <el-icon v-if="grandchild.icon" class="menu-icon"
                ><component :is="resolveIcon(grandchild.icon)"
              /></el-icon>
              <span v-show="!isCollapse" class="menu-label">{{ grandchild.title }}</span>
            </el-menu-item>
          </el-sub-menu>
          <!-- Otherwise, render a regular menu item (Child) -->
          <el-menu-item v-else :index="child.path">
            <el-icon v-if="child.icon" class="menu-icon"
              ><component :is="resolveIcon(child.icon)"
            /></el-icon>
            <span v-show="!isCollapse" class="menu-label">{{ child.title }}</span>
          </el-menu-item>
        </template>
      </el-sub-menu>
      <!-- Top Level Menu Item (No Children) -->
      <el-menu-item v-else :index="item.path">
        <el-icon v-if="item.icon" class="menu-icon"
          ><component :is="resolveIcon(item.icon)"
        /></el-icon>
        <span v-show="!isCollapse" class="menu-label">{{ item.label }}</span>
      </el-menu-item>
    </template>
  </el-menu>
</template>

<script setup>
  import { useRoute } from 'vue-router'
  import { computed } from 'vue'
  // Import all Element Plus icons if you are using string names in menus.js
  import * as ElementIcons from '@element-plus/icons-vue'

  const props = defineProps({
    menus: {
      type: Array,
      required: true,
    },
    isCollapse: {
      type: Boolean,
      default: false,
    },
  })

  const route = useRoute()

  // More robust active menu logic: checks current route and its parent paths
  const activeMenu = computed(() => {
    const { meta, path } = route
    // if set path, the sidebar will highlight the path you set
    if (meta.activeMenu) {
      return meta.activeMenu
    }
    // Check if parent path exists in menus to highlight parent sub-menu
    // This part might need adjustment based on your exact menu structure and routing
    for (let i = route.matched.length - 1; i >= 0; i--) {
      const matchedPath = route.matched[i].path
      // Check if any menu item or submenu exactly matches a path in the matched routes
      if (findMenuPath(props.menus, matchedPath)) {
        return matchedPath
      }
    }
    // Fallback to current path
    return path
  })

  // Helper function to find if a path exists in the menu structure
  // (Recursive check might be needed for deeper nesting if highlighting parents is complex)
  function findMenuPath(menuItems, path) {
    for (const item of menuItems) {
      if (item.path === path) return true
      if (item.children) {
        if (findMenuPath(item.children, path)) return true
      }
    }
    return false
  }

  // Function to resolve icon component from string name
  const resolveIcon = (iconName) => {
    // Check if the icon name exists in the imported ElementIcons object
    return ElementIcons[iconName] || null // Return the component or null
  }
</script>

<style scoped>
  /* Base Styles */
  .sidebar-menu {
    height: 100%;
    border-right: none !important; /* Override default el-menu border */
    transition: width 0.28s; /* Smooth collapse transition */
    overflow-x: hidden; /* Hide horizontal scrollbar during collapse */
    /* Set the expanded width */
    width: 210px; /* Default expanded width, adjust if needed */
  }

  /* Icon Styling */
  .beautify-sidebar .menu-icon {
    margin-right: 10px; /* Space between icon and text */
    font-size: 18px; /* Slightly larger icons */
    width: 24px; /* Ensure consistent icon alignment */
    text-align: center;
    vertical-align: middle;
    flex-shrink: 0; /* Prevent icon from shrinking */
    color: currentColor; /* Inherit color for better theme consistency */
  }

  .beautify-sidebar .menu-label {
    flex-grow: 1; /* Allow label to take remaining space */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .el-menu--collapse .menu-icon {
    margin: 0;
    font-size: 20px; /* Maybe slightly larger when collapsed */
    padding: 0 20px; /* Add some padding around the icon */
  }
</style>

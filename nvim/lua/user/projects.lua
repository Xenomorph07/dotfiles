local pickers = require("telescope.pickers")
local finders = require("telescope.finders")
local config = require("telescope.config").values
local actions = require("telescope.actions")
local action_state = require("telescope.actions.state")

local M = {}

local projects = vim.fn.systemlist("find ~/Code -mindepth 1 -maxdepth 1 -type d")

local function find_existing_tab(target)
  target = vim.fn.fnamemodify(target, ":p")
  for tabnr = 1, vim.fn.tabpagenr("$") do
    local tab_cwd = vim.fn.fnamemodify(vim.fn.getcwd(-1, tabnr), ":p")
    if tab_cwd == target then
      return tabnr
    end
  end

  return nil
end

function M.open_projects(opts)
  pickers
    .new(opts, {
      prompt_title = "Select Project",
      finder = finders.new_table({
        results = projects,
        entry_maker = function(entry)
          local name = vim.fn.fnamemodify(entry, ":t")
          return {
            value = entry,
            display = name,
            ordinal = name,
          }
        end,
      }),
      sorter = config.generic_sorter({}),
      attach_mappings = function(prompt_bufnr, _)
        actions.select_default:replace(function()
          actions.close(prompt_bufnr)
          local selection = action_state.get_selected_entry()
          local choice = selection.value
          local name = vim.fn.fnamemodify(choice, ":t")

          local found_tab = find_existing_tab(choice)

          if found_tab then
            vim.cmd("tabnext " .. found_tab)
            return
          end

          vim.cmd("tabnew")
          vim.cmd("Tabby rename_tab " .. name)
          vim.cmd("tcd " .. choice)
        end)
        return true
      end,
    })
    :find()
end

return M
